# ╔══════════════════════════════════════════════════════════════╗
# ║  CarryMe Store — AI Seller Intelligence                      ║
# ║  Deploy FREE · Streamlit Cloud · Gemini AI (Free Tier)      ║
# ╚══════════════════════════════════════════════════════════════╝

import streamlit as st
from PIL import Image
import io
import pandas as pd
import plotly.graph_objects as go

from config import (
    APP_NAME, PLATFORMS, SUPPLIERS_DB,
    SELLER_DOCS, INDIAN_STATES
)
from ai_engine import init_gemini, analyze_product_image
from state import init_state, save_analysis, register_user, increment_analysis_count

# ── PAGE CONFIG (must be first Streamlit call) ──────────────────
st.set_page_config(
    page_title="CarryMe Store — AI Seller Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.hero {
  background: linear-gradient(135deg,#667eea,#764ba2 50%,#f093fb);
  border-radius:16px; padding:2rem 2.5rem; color:white;
  margin-bottom:1.5rem; box-shadow:0 8px 32px rgba(102,126,234,.3);
}
.hero h1 { font-size:2.2rem; font-weight:700; margin:0; }
.hero p  { font-size:1rem; opacity:.9; margin:.4rem 0 0 0; }

.pcard {
  border:2px solid #f0f0f0; border-radius:14px; padding:1.2rem;
  margin-bottom:1rem; background:white;
  box-shadow:0 2px 12px rgba(0,0,0,.06);
  transition:all .2s;
}
.pcard.best { border-color:#667eea; border-width:3px; }

.scard {
  border-radius:12px; padding:1.1rem; margin-bottom:.8rem;
  background:#fafafa;
}
.scard.v  { border-left:4px solid #22c55e; }
.scard.uv { border-left:4px solid #f59e0b; }

.badge-g { background:#dcfce7;color:#15803d;padding:2px 10px;border-radius:20px;font-size:.8rem;font-weight:600; }
.badge-b { background:#dbeafe;color:#1d4ed8;padding:2px 10px;border-radius:20px;font-size:.8rem;font-weight:600; }
.badge-o { background:#ffedd5;color:#c2410c;padding:2px 10px;border-radius:20px;font-size:.8rem;font-weight:600; }

.ai-box {
  background:linear-gradient(135deg,#f8faff,#f0f4ff);
  border:1px solid #c7d2fe; border-radius:14px; padding:1.5rem; margin-bottom:1rem;
}
.step-box {
  background:linear-gradient(135deg,#667eea15,#764ba215);
  border-radius:10px; padding:1rem; text-align:center;
  border:1px solid #667eea30;
}
.info-box {
  background:#eff6ff; border-left:4px solid #3b82f6;
  border-radius:0 8px 8px 0; padding:.8rem 1rem;
  margin:.5rem 0; font-size:.9rem;
}
.key-ok {
  background:#f0fdf4; border:2px solid #22c55e;
  border-radius:10px; padding:.8rem 1rem; text-align:center;
  font-weight:600; color:#15803d; font-size:1rem;
}
.key-warn {
  background:#fffbeb; border:2px solid #f59e0b;
  border-radius:10px; padding:.8rem 1rem;
  font-size:.88rem; color:#92400e;
}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────
init_state()

# ── AUTO-LOAD API KEY FROM STREAMLIT SECRETS ────────────────────
# Tries all common secret key names so any format works
def _get_secret_key() -> str:
    """Read Gemini key from st.secrets — tries multiple key names."""
    for name in ["GEMINI_API_KEY", "gemini_api_key",
                 "GOOGLE_API_KEY", "google_api_key",
                 "GEMINI_KEY", "gemini_key"]:
        try:
            v = st.secrets[name]
            v = str(v).strip().strip('"').strip("'")
            v = v.strip().strip('"').strip("'")  # remove accidental quotes
            if len(v) > 15:
                return v
        except Exception:
            pass
    return ""

# Only load once per session
if not st.session_state.get("api_key"):
    _k = _get_secret_key()
    if _k:
        st.session_state.api_key = _k
        st.session_state.api_key_verified = True
        init_gemini(_k)

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛍️ CarryMe Store")
    st.markdown("*AI Intelligence for Indian Sellers*")
    st.divider()

    # ── API KEY STATUS ──
    st.markdown("### 🔑 Gemini API Key")

    _has_key = bool(st.session_state.get("api_key") and
                    st.session_state.get("api_key_verified"))

    if _has_key:
        st.markdown('<div class="key-ok">✅ AI Ready — Key Active</div>',
                    unsafe_allow_html=True)
        with st.expander("🔄 Replace Key"):
            _new = st.text_input("New key:", type="password",
                                 placeholder="AIzaSy...", key="_replace_key")
            if st.button("Update Key") and _new and len(_new.strip()) > 15:
                _k2 = _new.strip().strip('"').strip("'")
                st.session_state.api_key = _k2
                st.session_state.api_key_verified = True
                init_gemini(_k2)
                st.success("✅ Key updated!")
                st.rerun()
    else:
        # Show helper to get correct key
        st.markdown("""
<div class="key-warn">
⚠️ <b>No API key found.</b><br><br>
<b>Get your FREE Gemini key:</b><br>
1. Go to <a href="https://aistudio.google.com/app/apikey" target="_blank">
   aistudio.google.com/app/apikey</a><br>
2. Sign in with Google<br>
3. Click <b>"Create API Key"</b><br>
4. Key starts with <code>AIzaSy...</code>
</div>
""", unsafe_allow_html=True)
        st.markdown("")

        # Option A: paste in sidebar
        _manual = st.text_input("Paste key here:", type="password",
                                placeholder="AIzaSy...", key="_manual_key")
        if _manual:
            _k3 = _manual.strip().strip('"').strip("'")
            if not _k3.startswith("AIza") and len(_k3) < 20:
                st.error("❌ Wrong format. Gemini keys start with 'AIza'")
            elif len(_k3) > 15:
                st.session_state.api_key = _k3
                st.session_state.api_key_verified = True
                init_gemini(_k3)
                st.success("✅ Key loaded!")
                st.rerun()

        st.markdown("**Or** save it permanently in Streamlit Secrets:")
        st.code('GEMINI_API_KEY = "AIzaSy...yourkey"', language="toml")
        st.caption("App Settings → Secrets → paste the line above → Save")

    st.divider()

    # ── LOCATION ──
    st.markdown("### 📍 Your Location")
    _city = st.text_input("City / District",
                          value=st.session_state.get("user_city",""),
                          placeholder="e.g. Surat, Jaipur, Varanasi")
    _state_list = [""] + INDIAN_STATES
    _cur_state = st.session_state.get("user_state","")
    _state_idx = (_state_list.index(_cur_state)
                  if _cur_state in _state_list else 0)
    _state = st.selectbox("State", _state_list, index=_state_idx)
    if _city:  st.session_state.user_city  = _city
    if _state: st.session_state.user_state = _state

    st.divider()

    # ── STATS ──
    st.markdown("### 📊 Your Stats")
    c1, c2 = st.columns(2)
    c1.metric("Analyses", st.session_state.get("analysis_count", 0))
    c2.metric("Saved",    len(st.session_state.get("products_history", [])))

    _hist = st.session_state.get("products_history", [])
    if _hist:
        st.markdown("**Recent:**")
        for _p in _hist[-3:][::-1]:
            st.markdown(f"• {_p['product_name'][:22]}…")

    st.divider()
    st.caption("Free Tier: 15 analyses/min · Unlimited/day · ₹0 forever")

# ── HERO HEADER ──────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🛍️ CarryMe Store</h1>
  <p>📸 One Photo → Platform Intelligence · Bulk Suppliers · Business Setup</p>
  <p style="font-size:.82rem;opacity:.75;margin-top:.5rem;">
    Powered by Google Gemini AI · 100% Free · Built for Tier 3 &amp; 4 India
  </p>
</div>
""", unsafe_allow_html=True)

# ── UPLOAD SECTION ───────────────────────────────────────────────
st.markdown("## 📸 Upload Your Product Photo")

u_col, t_col = st.columns([2, 1])
with u_col:
    uploaded = st.file_uploader(
        "Upload a clear product image",
        type=["jpg","jpeg","png","webp"],
        help="Plain background, good lighting, 400×400px minimum"
    )
with t_col:
    st.markdown("""
<div class="step-box">
  <b>📸 Photo Tips</b><br><br>
  ✅ Plain white/light background<br>
  ✅ Good natural lighting<br>
  ✅ Product centered in frame<br>
  ❌ Avoid blurry / dark photos
</div>""", unsafe_allow_html=True)

# ── ANALYZE ──────────────────────────────────────────────────────
if uploaded:
    image = Image.open(uploaded)
    st.session_state.uploaded_image = image

    i_col, b_col = st.columns([1, 2])
    with i_col:
        st.image(image, caption="Your Product", use_container_width=True)

    with b_col:
        st.markdown("### 🤖 AI Analysis Ready")
        st.markdown(f"**File:** {uploaded.name}")
        st.markdown(f"**Size:** {image.size[0]}×{image.size[1]}px")

        _key_ok = bool(st.session_state.get("api_key") and
                       st.session_state.get("api_key_verified"))

        if not _key_ok:
            st.markdown("""
<div class="key-warn" style="margin-top:1rem;">
  ⚠️ <b>API key needed to analyze.</b><br><br>
  👈 Enter your Gemini key in the <b>sidebar</b>.<br><br>
  Get a free key at
  <a href="https://aistudio.google.com/app/apikey" target="_blank">
  aistudio.google.com/app/apikey</a><br>
  (Google sign-in → Create API Key → starts with <code>AIzaSy...</code>)
</div>""", unsafe_allow_html=True)
        else:
            if st.button("🔍 Analyze Product (AI)",
                         type="primary", use_container_width=True):
                _bar = st.progress(0, text="📤 Sending image to Gemini AI…")
                _msg = st.empty()
                try:
                    _bar.progress(25, text="🤖 Gemini is reading your product…")
                    _result = analyze_product_image(
                        image,
                        st.session_state.get("user_city",""),
                        st.session_state.get("user_state","")
                    )
                    _bar.progress(85, text="✍️ Building your insights…")
                    st.session_state.analysis_result = _result

                    if _result.get("success"):
                        _bar.progress(100, text="✅ Done!")
                        increment_analysis_count()
                        save_analysis(_result, uploaded.name)
                        _msg.success("✅ Analysis complete! Scroll down ↓")
                        st.balloons()
                    else:
                        _bar.empty()
                        _err = _result.get("error","Analysis failed.")
                        if _result.get("rate_limited"):
                            _msg.warning(f"{_err}\n\n⏳ Wait 60 seconds then try again.")
                        else:
                            _msg.error(_err)
                            st.info("💡 **Fix:** Check your API key · Use clearer photo · "
                                    "Enable Gemini at [aistudio.google.com](https://aistudio.google.com)")
                except Exception as _ex:
                    _bar.empty()
                    _msg.error(f"⚠️ Error: {str(_ex)[:250]}")

# ── RESULTS TABS ─────────────────────────────────────────────────
_res = st.session_state.get("analysis_result")

if _res and _res.get("success"):
    _cat = _res.get("category","General")
    _pname = _res.get("product_name","Your Product")

    st.markdown("---")
    st.markdown(f"""
<div class="ai-box">
  <h3>🎯 {_pname}</h3>
  <p><b>Category:</b> {_cat} &nbsp;|&nbsp;
     <b>Sub:</b> {_res.get('sub_category','—')} &nbsp;|&nbsp;
     <b>Origin:</b> {_res.get('origin_hint','Indian Craft')}</p>
  <p><b>Suggested Price:</b>
     ₹{_res.get('price_suggestion',{}).get('min',0)} –
     ₹{_res.get('price_suggestion',{}).get('max',0)} INR</p>
  <p><b>💡 Tip:</b> {_res.get('seller_tip','')}</p>
</div>
""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "🏆 Tab 1 — Platform Intelligence",
        "📦 Tab 2 — Bulk Suppliers & Contacts",
        "🚀 Tab 3 — Register Seller / Buyer"
    ])

    # ══════════════════════════════════════
    # TAB 1 — PLATFORM INTELLIGENCE
    # ══════════════════════════════════════
    with tab1:
        st.markdown(f"## 🏆 Best Platforms for Your Product")
        st.markdown(f"*Product: **{_pname}** · Category: **{_cat}***")

        _pdata = []
        for _pn, _pi in PLATFORMS.items():
            _cd = _pi["categories"].get(_cat, _pi["categories"]["General"])
            _pdata.append({
                "name":_pn, "score":_cd["score"],
                "rating":_cd["avg_rating"], "reviews":_cd["reviews"],
                "commission":_pi["commission"],
                "price_range":_cd["price_range"],
                "orders":_cd["orders_range"],
                "logo":_pi["logo"], "color":_pi["color"],
                "url":_pi["signup_url"],
                "pros":_pi["pros"], "cons":_pi["cons"],
                "gst":_pi["gst_required"],
            })
        _pdata.sort(key=lambda x: x["score"], reverse=True)

        # Bar chart
        _fig = go.Figure(go.Bar(
            x=[p["name"] for p in _pdata],
            y=[p["score"] for p in _pdata],
            marker_color=[p["color"] for p in _pdata],
            text=[f"{p['score']}%" for p in _pdata],
            textposition="outside",
        ))
        _fig.update_layout(
            title=f"Platform Match Score for '{_cat}'",
            yaxis_title="Match %", yaxis_range=[0,105],
            showlegend=False, height=260,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(_fig, use_container_width=True)

        # Platform cards
        for _i, _p in enumerate(_pdata):
            _best = (_i == 0)
            _lc, _dc, _bc = st.columns([1, 3, 1.5])

            with _lc:
                st.markdown(
                    f"<div style='font-size:3rem;text-align:center;padding-top:.5rem'>"
                    f"{_p['logo']}</div>", unsafe_allow_html=True)
                if _best:
                    st.markdown(
                        "<div style='text-align:center'>"
                        "<span class='badge-g'>🏅 BEST MATCH</span></div>",
                        unsafe_allow_html=True)
                st.markdown(
                    f"<div style='text-align:center;font-size:1.3rem;"
                    f"font-weight:700;color:{_p['color']}'>{_p['score']}%</div>",
                    unsafe_allow_html=True)

            with _dc:
                st.markdown(f"### {_p['name']}")
                _m1,_m2,_m3 = st.columns(3)
                _m1.metric("⭐ Rating",     _p["rating"])
                _m2.metric("📝 Reviews",   f"{_p['reviews']:,}")
                _m3.metric("💸 Commission",f"{_p['commission']}%")
                _m4,_m5 = st.columns(2)
                _m4.metric("💰 Price",
                           f"₹{_p['price_range'][0]}–₹{_p['price_range'][1]}")
                _m5.metric("📦 Est.Orders", _p["orders"])
                _gb = "badge-o" if _p["gst"] else "badge-g"
                _gt = "⚠️ GST Needed" if _p["gst"] else "✅ No GST"
                st.markdown(f"<span class='{_gb}'>{_gt}</span>",
                            unsafe_allow_html=True)
                with st.expander("Pros & Cons"):
                    _pa, _pb = st.columns(2)
                    with _pa:
                        st.markdown("**✅ Pros:**")
                        for _x in _p["pros"]: st.markdown(f"• {_x}")
                    with _pb:
                        st.markdown("**❌ Cons:**")
                        for _x in _p["cons"]: st.markdown(f"• {_x}")

            with _bc:
                st.markdown("<br>", unsafe_allow_html=True)
                st.link_button("Register as Seller →", _p["url"],
                               use_container_width=True,
                               type="primary" if _best else "secondary")
            st.divider()

        # AI-generated listing
        st.markdown("### ✍️ Your AI-Generated Listing")
        _lc1, _lc2 = st.columns(2)
        with _lc1:
            st.markdown("**📋 Listing Title:**")
            st.code(_res.get("listing_title",""), language=None)
            st.markdown("**🏷️ SEO Tags:**")
            st.code(", ".join(_res.get("seo_tags",[])), language=None)
        with _lc2:
            st.markdown("**📝 Description:**")
            st.text_area("", value=_res.get("listing_description",""),
                         height=200, label_visibility="collapsed")

        _usps = _res.get("unique_selling_points",[])
        if _usps:
            st.markdown("**🌟 Unique Selling Points:**")
            _uc = st.columns(len(_usps))
            for _i,_u in enumerate(_usps):
                _uc[_i].markdown(
                    f"<div class='step-box'>🎯 {_u}</div>",
                    unsafe_allow_html=True)

    # ══════════════════════════════════════
    # TAB 2 — SUPPLIERS
    # ══════════════════════════════════════
    with tab2:
        st.markdown("## 📦 Raw Material Suppliers & Bulk Contacts")
        _loc_display = (f"{st.session_state.get('user_city','')}, "
                        f"{st.session_state.get('user_state','')}").strip(", ") or "All India"
        st.markdown(f"*Category: **{_cat}** · Your location: **{_loc_display}***")

        _loc_q = st.text_input(
            "🔍 Search suppliers by city/state:",
            placeholder="e.g. Mumbai, Rajasthan, Gujarat", key="sup_loc")
        _search = _loc_q.lower().strip() if _loc_q else \
                  st.session_state.get("user_city","").lower()

        _sups = SUPPLIERS_DB.get(_cat, SUPPLIERS_DB.get("General",[]))
        if _search:
            _filtered = [s for s in _sups
                         if _search in s["city"].lower()
                         or _search in s["state"].lower()]
            if not _filtered:
                st.info(f"No suppliers found for '{_loc_q}'. Showing all.")
                _filtered = _sups
        else:
            _filtered = _sups

        _v = sum(1 for s in _filtered if s["verified"])
        st.markdown(f"**{len(_filtered)} suppliers found** · {_v} verified ✅")
        st.divider()

        for _s in _filtered:
            _cls = "v" if _s["verified"] else "uv"
            _vlabel = ("✅ Verified" if _s["verified"]
                       else "⚠️ Unverified — confirm before ordering")
            _si, _sm, _sc = st.columns([2.5,1.5,1.5])

            with _si:
                st.markdown(f"#### 🏭 {_s['name']}")
                st.markdown(f"📍 **{_s['city']}, {_s['state']}**")
                st.markdown(f"🔧 {_s['type']}")
                _bc2 = "badge-g" if _s["verified"] else "badge-o"
                st.markdown(f"<span class='{_bc2}'>{_vlabel}</span>",
                            unsafe_allow_html=True)
            with _sm:
                st.markdown("**📦 MOQ:**")
                st.markdown(f"Min: **{_s['moq']}**")
                st.markdown(f"Price: **{_s['price']}**")
            with _sc:
                _wa = (f"https://wa.me/{_s['whatsapp']}"
                       f"?text=Hi%2C+I+need+{_cat.replace(' ','+')}+"
                       f"in+bulk.+Please+share+MOQ+and+price+details.")
                st.link_button("💬 WhatsApp",  _wa,              use_container_width=True)
                st.link_button("🗺️ Map",       _s["maps_url"],   use_container_width=True)
            st.divider()

        st.markdown("### 🌐 Search More on B2B Platforms")
        _b1,_b2,_b3 = st.columns(3)
        with _b1:
            st.markdown('<div class="step-box"><b>🇮🇳 IndiaMART</b><br>'
                        'India\'s largest B2B · 10M+ suppliers</div>',
                        unsafe_allow_html=True)
            st.link_button(
                "Search IndiaMART →",
                f"https://www.indiamart.com/search.mp?ss={_cat.replace(' ','+')}",
                use_container_width=True)
        with _b2:
            st.markdown('<div class="step-box"><b>🔄 TradeIndia</b><br>'
                        'Pan-India wholesale · 3M+ suppliers</div>',
                        unsafe_allow_html=True)
            st.link_button("Search TradeIndia →",
                           "https://www.tradeindia.com",
                           use_container_width=True)
        with _b3:
            st.markdown('<div class="step-box"><b>🏛️ MSME Clusters</b><br>'
                        'Govt-verified artisan clusters</div>',
                        unsafe_allow_html=True)
            st.link_button("MSME Directory →",
                           "https://msme.gov.in/1-industrial-clusters",
                           use_container_width=True)

        # WhatsApp template
        st.markdown("### 📋 Ready-to-Send WhatsApp Template")
        _mats = ", ".join(_res.get("materials",["raw materials"]))
        _tmpl = (f"Hi,\n\nI am a small handmade seller looking for "
                 f"bulk {_cat} materials.\n\n"
                 f"Product: {_pname}\nMaterials: {_mats}\n"
                 f"Location: {_loc_display}\n\n"
                 f"Please share:\n• MOQ (minimum order)\n"
                 f"• Price per unit\n• Delivery time\n• Payment terms\n\nThank you!")
        st.text_area("Copy & send on WhatsApp:", value=_tmpl, height=220)

    # ══════════════════════════════════════
    # TAB 3 — REGISTRATION
    # ══════════════════════════════════════
    with tab3:
        st.markdown("## 🚀 One-Click Business Setup")
        _r1,_r2,_r3 = st.tabs(["📋 Docs Checklist",
                                "👤 Seller Registration",
                                "🛒 Buyer Registration"])

        with _r1:
            st.markdown("### 📋 Documents You Need to Start Selling")
            for _d in SELLER_DOCS:
                _dc1,_dc2,_dc3 = st.columns([.5,2,3])
                with _dc1: st.checkbox("", key=f"doc_{_d['doc']}")
                with _dc2:
                    _rb = "badge-o" if _d["required"] else "badge-b"
                    _rl = "🔴 Required" if _d["required"] else "🟡 Optional"
                    st.markdown(f"**{_d['doc']}**")
                    st.markdown(f"<span class='{_rb}'>{_rl}</span>",
                                unsafe_allow_html=True)
                with _dc3:
                    st.markdown(f"*{_d['note']}*")
                st.divider()

            st.markdown("### 🔗 Register Directly")
            _rp1,_rp2,_rp3 = st.columns(3)
            with _rp1:
                st.markdown("**🛍️ Meesho**\nNo GST · No listing fee")
                st.link_button("Register →","https://supplier.meesho.com",
                               use_container_width=True, type="primary")
            with _rp2:
                st.markdown("**⭐ Flipkart**\nEkart logistics · PAN needed")
                st.link_button("Register →","https://seller.flipkart.com",
                               use_container_width=True)
            with _rp3:
                st.markdown("**📦 Amazon India**\nFBA available · GST preferred")
                st.link_button("Register →","https://sell.amazon.in",
                               use_container_width=True)

            st.markdown("---")
            st.markdown("### 🏛️ Government Schemes")
            _gs1,_gs2 = st.columns(2)
            with _gs1:
                st.markdown("**📜 Udyam (Free MSME)**\n"
                            "Priority loans · Scheme access")
                st.link_button("Register →",
                               "https://udyamregistration.gov.in",
                               use_container_width=True)
            with _gs2:
                st.markdown("**🎨 Craft Board**\n"
                            "GI Tag · Export access")
                st.link_button("Explore →",
                               "https://www.craftcouncilofindia.org",
                               use_container_width=True)

        with _r2:
            st.markdown("### 👤 Register as a CarryMe Seller")
            with st.form("seller_form"):
                _sc1,_sc2 = st.columns(2)
                with _sc1:
                    _sn = st.text_input("Full Name *", placeholder="Priya Sharma")
                    _sp = st.text_input("Mobile *", placeholder="9876543210")
                    _sci= st.text_input("City *",
                                        value=st.session_state.get("user_city",""),
                                        placeholder="Surat")
                with _sc2:
                    _ss = st.selectbox("State *", ["Select"]+INDIAN_STATES)
                    _sc = st.selectbox("Category *",
                                       list(PLATFORMS["Meesho"]["categories"].keys()))
                    _sm = st.multiselect("Platforms:", ["Meesho","Flipkart","Amazon India"],
                                         default=["Meesho"])
                _spr = st.text_input("Product Name", value=_pname)
                _sb  = st.text_input("Business/Store Name (optional)",
                                     placeholder="e.g. Priya Crafts")
                _se  = st.radio("Experience:", ["New","1–2 years","3+ years"],
                                horizontal=True)
                _sa  = st.checkbox("I agree to CarryMe terms & privacy policy")
                _sub = st.form_submit_button("🚀 Create Seller Account",
                                             type="primary", use_container_width=True)
                if _sub:
                    if not _sn or not _sp or _ss == "Select":
                        st.error("Fill all required (*) fields.")
                    elif not _sa:
                        st.warning("Please agree to terms.")
                    else:
                        _sdata = {"name":_sn,"phone":_sp,"city":_sci,
                                  "state":_ss,"category":_sc,"platforms":_sm,
                                  "product":_spr,"business":_sb or f"{_sn} Crafts",
                                  "experience":_se}
                        register_user("seller", _sdata)
                        st.success(f"🎉 Welcome {_sn}! Seller ID: {_sdata.get('id','S1001')}")
                        st.balloons()

        with _r3:
            st.markdown("### 🛒 Register as a Buyer")
            with st.form("buyer_form"):
                _bc1,_bc2 = st.columns(2)
                with _bc1:
                    _bn = st.text_input("Full Name *", placeholder="Rahul Kumar")
                    _bph= st.text_input("Mobile *", placeholder="9876543210")
                    _bc_= st.text_input("City *", placeholder="Mumbai")
                with _bc2:
                    _bs = st.selectbox("State *", ["Select"]+INDIAN_STATES,
                                       key="buyer_state")
                    _bi = st.multiselect("Interests:",
                                         list(PLATFORMS["Meesho"]["categories"].keys()))
                    _bb = st.select_slider("Budget per item (₹):",
                                           [50,100,200,500,1000,2000,5000], value=500)
                _bp  = st.radio("Buying for:",
                                ["Personal","Gift","Resale","Decoration"],
                                horizontal=True)
                _ba  = st.checkbox("I agree to buyer terms")
                _bsub= st.form_submit_button("🛒 Create Buyer Account",
                                              type="primary", use_container_width=True)
                if _bsub:
                    if not _bn or not _bph or _bs == "Select":
                        st.error("Fill all required (*) fields.")
                    elif not _ba:
                        st.warning("Please agree to terms.")
                    else:
                        _bdata = {"name":_bn,"phone":_bph,"city":_bc_,
                                  "state":_bs,"interests":_bi,
                                  "budget":_bb,"purpose":_bp}
                        register_user("buyer", _bdata)
                        st.success(f"🎉 Welcome {_bn}! Buyer ID: {_bdata.get('id','B1001')}")

# ── EMPTY STATE ──────────────────────────────────────────────────
elif not uploaded:
    st.markdown("---")
    st.markdown("### 🌟 How CarryMe Store Works")
    _h1,_h2,_h3 = st.columns(3)
    with _h1:
        st.markdown("""<div class="step-box">
          <div style="font-size:2.5rem">📸</div>
          <h4>Step 1: Upload Photo</h4>
          <p>Click or upload your handmade product. Good natural light works great!</p>
        </div>""", unsafe_allow_html=True)
    with _h2:
        st.markdown("""<div class="step-box">
          <div style="font-size:2.5rem">🤖</div>
          <h4>Step 2: AI Analysis</h4>
          <p>Gemini identifies product, generates SEO listing, finds best platform match.</p>
        </div>""", unsafe_allow_html=True)
    with _h3:
        st.markdown("""<div class="step-box">
          <div style="font-size:2.5rem">🚀</div>
          <h4>Step 3: Go Live!</h4>
          <p>Platform ratings, bulk suppliers, seller registration — all in one click.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Platform Quick Comparison")
    _df = pd.DataFrame([
        {"Platform":"Meesho 🛍️","Commission":"1.8%",
         "GST Needed":"No","Best For":"High volume ethnic goods","Tier":"2/3/4 cities"},
        {"Platform":"Flipkart ⭐","Commission":"8.5%",
         "GST Needed":"No*","Best For":"Mid-range branded look","Tier":"Pan India"},
        {"Platform":"Amazon India 📦","Commission":"10%",
         "GST Needed":"Preferred","Best For":"Premium & export","Tier":"Urban premium"},
    ])
    st.dataframe(_df, use_container_width=True, hide_index=True)
    st.markdown("""<div class="info-box">
      💡 <b>Start with Meesho</b> — lowest commission (1.8%), no GST, largest
      Tier 3/4 buyer base. Once you have 20+ reviews, expand to Flipkart & Amazon.
    </div>""", unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#888;font-size:.82rem;padding:1rem">
  🛍️ <b>CarryMe Store</b> · AI-Powered Seller Intelligence for Indian Handmade Products<br>
  Built with ❤️ for Tier 3 &amp; 4 India · Google Gemini AI (Free) · Streamlit Cloud<br>
  <small>Not affiliated with Meesho, Flipkart or Amazon. Data is indicative.</small>
</div>
""", unsafe_allow_html=True)
