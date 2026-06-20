# ai_engine.py — Gemini AI Vision Engine (FREE API) — using google-genai SDK
from google import genai
from google.genai import types
from PIL import Image
import json
import re
import io
import base64


_client = None

def init_gemini(api_key: str):
    """Initialize Gemini client with the provided API key."""
    global _client
    _client = genai.Client(api_key=api_key)


def _image_to_bytes(image: Image.Image) -> bytes:
    """Convert PIL image to bytes."""
    buf = io.BytesIO()
    fmt = image.format if image.format else "JPEG"
    if fmt not in ("JPEG", "PNG", "WEBP"):
        fmt = "JPEG"
    image.save(buf, format=fmt)
    return buf.getvalue()


def analyze_product_image(image: Image.Image, user_city: str = "", user_state: str = "") -> dict:
    """
    Send product image to Gemini Vision for deep analysis.
    Returns structured product intelligence.
    """
    global _client
    if _client is None:
        return {"success": False, "error": "❌ API client not initialized. Please enter your Gemini API key."}

    prompt = f"""You are an expert Indian e-commerce product analyst specializing in handmade, artisan, and small-scale manufactured goods for platforms like Meesho, Flipkart, and Amazon India.

Analyze this product image and return ONLY a JSON object (no markdown, no explanation, just raw JSON).

The JSON must follow this exact structure:
{{
  "product_name": "Clear descriptive product name (e.g., Hand-Embroidered Cotton Dupatta)",
  "category": "One of: Fashion & Apparel, Ethnic Wear, Handmade Jewelry, Home Decor, Handicrafts, Bags & Accessories, Candles & Aroma, Paintings & Art, Toys & Kids, General",
  "sub_category": "More specific category (e.g., Embroidered Dupatta)",
  "materials": ["material1", "material2"],
  "colors": ["color1", "color2"],
  "style_keywords": ["keyword1", "keyword2", "keyword3"],
  "confidence": 0.90,
  "listing_title": "SEO-optimized product title under 80 chars for Indian market",
  "listing_description": "Compelling product description under 200 words highlighting handmade quality, cultural significance, and buyer benefits. Indian market focused.",
  "price_suggestion": {{
    "min": 150,
    "max": 500,
    "currency": "INR",
    "reasoning": "Brief reason for price range"
  }},
  "target_buyer": "Description of ideal buyer persona",
  "unique_selling_points": ["USP1", "USP2", "USP3"],
  "seo_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "platform_recommendation": "Meesho",
  "seller_tip": "One actionable tip for this seller in simple language",
  "origin_hint": "Likely craft tradition or origin if recognizable (e.g., Rajasthani, Bengali, South Indian)"
}}

User location: {user_city}, {user_state if user_state else 'India'}

Be specific, practical, and focus on what works for small Indian handmade sellers. If you cannot clearly identify the product, make your best assessment based on visible details."""

    try:
        img_bytes = _image_to_bytes(image)
        mime = "image/jpeg"
        if image.format == "PNG":
            mime = "image/png"
        elif image.format == "WEBP":
            mime = "image/webp"

        response = _client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type=mime),
                types.Part.from_text(text=prompt),
            ]
        )

        raw = response.text.strip()
        # Clean markdown fences
        raw = re.sub(r"```json\s*", "", raw)
        raw = re.sub(r"```\s*", "", raw)
        raw = raw.strip()

        result = json.loads(raw)
        result["success"] = True
        return result

    except json.JSONDecodeError:
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                result = json.loads(match.group())
                result["success"] = True
                return result
        except Exception:
            pass
        return {
            "success": False,
            "error": "Could not parse AI response. Please try again with a clearer image.",
        }

    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "invalid" in error_msg.lower() or "api key" in error_msg.lower():
            return {"success": False, "error": "❌ Invalid API Key. Please check your Gemini API key in the sidebar."}
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower() or "429" in error_msg:
            return {"success": False, "error": "⏳ API quota reached. Free tier allows 15 requests/minute. Please wait and try again."}
        else:
            return {"success": False, "error": f"AI Error: {error_msg[:300]}"}


def generate_morning_briefing(products_analyzed: list) -> str:
    """Generate a seller morning briefing using Gemini text."""
    global _client
    if _client is None or not products_analyzed:
        return "No products analyzed yet today."

    prompt = f"""You are a helpful business advisor for small Indian handmade product sellers.

Based on these recently analyzed products: {json.dumps(products_analyzed[:5])}

Write a brief, encouraging morning business briefing in simple English (2-3 sentences) with:
1. A key insight about their product category
2. One actionable tip to boost sales today
3. A motivating closing line

Keep it warm, practical, and under 100 words. Use simple language suitable for Tier 3/4 city sellers."""

    try:
        response = _client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception:
        return "🌅 Good morning! Your handmade products have unique value. Focus on clear photos and honest descriptions to win buyers' trust today. Every sale starts with a great product image!"
