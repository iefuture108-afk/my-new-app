# ai_engine.py — Gemini AI Vision Engine
# Free tier: gemini-2.0-flash · 15 req/min · 1500 req/day

from google import genai
from google.genai import types
from PIL import Image
import json
import re
import io
import time

_client = None
_last_call_time = 0


def init_gemini(api_key: str):
    """Initialize Gemini client with API key."""
    global _client
    _client = genai.Client(api_key=api_key.strip())


def _resize_image(image: Image.Image) -> tuple:
    """Resize to max 1024px and convert to JPEG bytes for API efficiency."""
    MAX = 1024
    w, h = image.size
    if w > MAX or h > MAX:
        ratio = min(MAX / w, MAX / h)
        image = image.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    # Normalize mode for JPEG
    if image.mode in ("RGBA", "P", "LA"):
        image = image.convert("RGB")

    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=85)
    return buf.getvalue(), "image/jpeg"


def _is_rate_limit_error(e: Exception) -> bool:
    """Detect true rate limit (429 / RESOURCE_EXHAUSTED) - NOT other errors."""
    msg = str(e).lower()
    return (
        "429" in str(e) or
        "resource_exhausted" in msg or
        "too_many_requests" in msg or
        "toomanyrequests" in msg or
        (("quota" in msg or "rate limit" in msg) and "429" in str(e))
    )


def _is_auth_error(e: Exception) -> bool:
    """Detect API key / auth errors."""
    msg = str(e).lower()
    return (
        "400" in str(e) and ("api_key" in msg or "api key" in msg) or
        "401" in str(e) or
        "invalid api key" in msg or
        "api_key_invalid" in msg
    )


def _call_with_retry(contents, max_retries: int = 3) -> str:
    """Call Gemini API with exponential backoff on true rate limits only."""
    global _client, _last_call_time

    # Gentle pacing — don't hammer the free tier
    gap = time.time() - _last_call_time
    if gap < 2.0:
        time.sleep(2.0 - gap)

    for attempt in range(max_retries):
        try:
            _last_call_time = time.time()
            response = _client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
            )
            return response.text.strip()

        except Exception as e:
            if _is_rate_limit_error(e) and attempt < max_retries - 1:
                wait_sec = (2 ** attempt) * 5  # 5s → 10s → 20s
                time.sleep(wait_sec)
                continue
            raise  # non-rate-limit errors or final attempt: propagate


def analyze_product_image(image: Image.Image, user_city: str = "", user_state: str = "") -> dict:
    """
    Analyze a product image with Gemini Vision.
    Returns structured JSON for all 3 CarryMe tabs.
    """
    if _client is None:
        return {
            "success": False,
            "error": "❌ API key not set. Please paste your Gemini key in the sidebar."
        }

    location = f"{user_city}, {user_state}".strip(", ") or "India"

    prompt = f"""You are an expert Indian e-commerce product analyst for Meesho, Flipkart, and Amazon India.

Analyze this product image. Return ONLY a valid JSON object — no markdown, no backticks, no text before or after.

JSON structure (fill every field):
{{
  "product_name": "Short descriptive name e.g. Hand-Embroidered Cotton Dupatta",
  "category": "Exactly one of: Fashion & Apparel | Ethnic Wear | Handmade Jewelry | Home Decor | Handicrafts | Bags & Accessories | Candles & Aroma | Paintings & Art | Toys & Kids | General",
  "sub_category": "e.g. Embroidered Dupatta",
  "materials": ["list", "of", "materials"],
  "colors": ["primary", "secondary"],
  "style_keywords": ["keyword1", "keyword2", "keyword3"],
  "confidence": 0.90,
  "listing_title": "SEO title max 80 chars, Indian market",
  "listing_description": "150-200 words. Mention handmade quality, cultural value, occasion use. Simple English.",
  "price_suggestion": {{
    "min": 150,
    "max": 500,
    "currency": "INR",
    "reasoning": "One sentence justification"
  }},
  "target_buyer": "Who buys this e.g. Women 25-45 who love ethnic wear",
  "unique_selling_points": ["USP1", "USP2", "USP3"],
  "seo_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "platform_recommendation": "Meesho",
  "seller_tip": "One practical tip in plain English for a small Indian seller",
  "origin_hint": "Craft region/tradition if visible, else empty string"
}}

Seller is based in: {location}
Give practical advice for Tier 3/4 Indian handmade sellers selling online for the first time."""

    try:
        img_bytes, mime = _resize_image(image)
        raw = _call_with_retry([
            types.Part.from_bytes(data=img_bytes, mime_type=mime),
            types.Part.from_text(text=prompt),
        ])

        # Strip accidental markdown fences
        raw = re.sub(r"^```[a-zA-Z]*\s*", "", raw.strip(), flags=re.MULTILINE)
        raw = re.sub(r"\s*```$", "", raw.strip(), flags=re.MULTILINE)
        raw = raw.strip()

        # Parse JSON
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r'\{[\s\S]*\}', raw)
            if match:
                result = json.loads(match.group())
            else:
                return {
                    "success": False,
                    "error": "🔄 AI returned unexpected format. Try again with a clearer photo on a plain background."
                }

        result["success"] = True
        return result

    except Exception as e:
        msg = str(e)

        if _is_auth_error(e):
            return {
                "success": False,
                "error": "❌ Invalid API key. Get your free key at aistudio.google.com/app/apikey"
            }
        elif _is_rate_limit_error(e):
            return {
                "success": False,
                "error": "⏳ Rate limit hit (15 req/min on free tier). Wait 60 seconds and try again.",
                "rate_limited": True
            }
        elif "403" in msg and "allowlist" in msg.lower():
            return {
                "success": False,
                "error": "🔒 Network blocked. If running locally, check firewall. On Streamlit Cloud this should work — try redeploying."
            }
        elif "403" in msg:
            return {
                "success": False,
                "error": "🔒 API access denied. Ensure Gemini API is enabled at aistudio.google.com"
            }
        elif "timeout" in msg.lower() or "timed out" in msg.lower():
            return {
                "success": False,
                "error": "⌛ Request timed out. Please try again."
            }
        else:
            return {
                "success": False,
                "error": f"⚠️ Unexpected error: {msg[:200]}"
            }


def generate_morning_briefing(products_analyzed: list) -> str:
    """Generate a short seller tip from recent history. Text-only, minimal quota use."""
    if _client is None or not products_analyzed:
        return "Upload a product photo to get your AI-powered business intelligence!"

    prompt = f"""You are a friendly business advisor for small Indian handmade sellers.

Recent products: {json.dumps(products_analyzed[:3])}

In 2 sentences max (under 60 words): give one practical tip to sell more of these products online in India. 
Be warm, specific, and encouraging. Plain English only."""

    try:
        return _call_with_retry(prompt)
    except Exception:
        return "🌅 Your handmade craft is unique — no factory can copy your skill! Clear photos with natural light are your best tool. Your first online sale is closer than you think! 💪"
