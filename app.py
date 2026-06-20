import streamlit as st
from PIL import Image
import io
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from config import (
    APP_NAME, APP_TAGLINE, PLATFORMS, SUPPLIERS_DB,
    SELLER_DOCS, INDIAN_STATES
)
from ai_engine import init_gemini, analyze_product_image
from state import init_state, save_analysis, register_user, increment_analysis_count

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="CarryMe Store — AI Seller Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
  /* Import Google Font */
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
  }

  /* Hero gradient header */
  .hero-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  }
  .hero-header h1 { font-size: 2.2rem; font-weight: 700; margin: 0; }
  .hero-header p { font-size: 1.05rem; opacity: 0.9; margin: 0.4rem 0 0 0; }

  /* Platform cards */
  .platform-card {
    border: 2px solid #f0f0f0;
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    background: white;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: all 0.2s ease;
  }
  .platform-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.12); transform: translateY(-2px); }
  .platform-card.top-pick { border-color: #667eea; border-width: 3px; }

  /* Supplier cards */
  .supplier-card {
    border: 1px solid #e8e8e8;
    border-radius: 12px;
    padding: 1.1rem;
    margin-bottom: 0.8rem;
    background: #fafafa;
  }
  .supplier-card.verified { border-left: 4px solid #22c55e; }
  .supplier-card.unverified { border-left: 4px solid #f59e0b; }

  /* Metric badges */
  .badge-green { background: #dcfce7; color: #15803d; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
  .badge-blue { background: #dbeafe; color: #1d4ed8; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
  .badge-orange { background: #ffedd5; color: #c2410c; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
  .badge-purple { background: #f3e8ff; color: #7e22ce; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }

  /* Step indicators */
  .step-box {
    background: linear-gradient(135deg, #667eea15, #764ba215);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #667eea30;
  }

  /* AI result card */
  .ai-result {
    background: linear-gradient(135deg, #f8faff, #f0f4ff);
    border: 1px solid #c7d2fe;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
  }

  /* Tabs styling */
  .stTabs [data-baseweb="tab-list"] { gap: 8px; }
  .stTabs [data-baseweb="tab"] {
    font-weight: 600;
    font-size: 0.95rem;
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
  }

  /* Warning/info boxes */
  .info-box {
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
  }

  /* Button override */
  .stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s;
  }

  /* Hide Streamlit branding */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# INIT STATE
# ─────────────────────────────────────────
init_state()

# ─────────────────────────────────────────
# SIDEBAR — API KEY + LOCATION
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛍️ CarryMe Store")
    st.markdown("*AI Business Intelligence for Indian Sellers*")
    st.divider()

    # API Key input
    st.markdown("### 🔑 Gemini API Key")
    st.markdown('<div class="info-box">Get your <b>FREE</b> key at <a href="https://aistudio.google.com/app/apikey" target="_blank">aistudio.google.com</a> · 15 req/min free</div>', unsafe_allow_html=True)

    api_key_input = st.text_input(
        "Enter Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="AIza...",
        help="Google AI Studio free API key"
    )

    if api_key_input:
        st.session_state.api_key = api_key_input
        init_gemini(api_key_input)
        st.session_state.api_key_verified = True
        st.success("✅ API Key loaded!")

    st.divider()

    # Location
    st.markdown("### 📍 Your Location")
    city = st.text_input("City / District", value=st.session_state.user_city, placeholder="e.g., Surat, Jaipur, Varanasi")
    state = st.selectbox("State", [""] + INDIAN_STATES, index=0 if not st.session_state.user_state else (INDIAN_STATES.index(st.session_state.user_state) + 1 if st.session_state.user_state in INDIAN_STATES else 0))

    if city: st.session_state.user_city = city
    if state: st.session_state.user_state = state

    st.divider()

    # Stats
    st.markdown("### 📊 Your Stats")
    col1, col2 = st.columns(2)
    col1.metric("Analyses", st.session_state.analysis_count)
    col2.metric("Saved", len(st.session_state.products_history))

    if st.session_state.products_history:
        st.markdown("**Recent Products:**")
        for p in st.session_state.products_history[-3:][::-1]:
            st.markdown(f"• {p['product_name'][:25]}...")

    st.divider()
    st.markdown("**Free Tier Limits:**")
    st.markdown("• 15 analyses/minute")
    st.markdown("• Unlimited/day")
    st.markdown("• 100% free forever")

# ─────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
  <h1>🛍️ {APP_NAME}</h1>
  <p>📸 One Photo → Platform Intelligence · Bulk Suppliers · Business Setup</p>
  <p style="font-size:0.85rem;opacity:0.75;margin-top:0.5rem;">Powered by Google Gemini AI · 100% Free · Built for Tier 3 & 4 India</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# IMAGE UPLOAD SECTION
# ─────────────────────────────────────────
st.markdown("## 📸 Upload Your Product Photo")

upload_col, tip_col = st.columns([2, 1])

with upload_col:
    uploaded_file = st.file_uploader(
        "Upload a clear product image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Plain background photos work best. Min 400x400px."
    )

with tip_col:
    st.markdown("""
    <div class="step-box">
      <b>📸 Photo Tips</b><br><br>
      ✅ Plain white/light background<br>
      ✅ Good natural lighting<br>
      ✅ Product centered in frame<br>
      ✅ Multiple angles if possible<br>
      ❌ Avoid blurry or dark photos
    </div>
    """, unsafe_allow_html=True)

# Show uploaded image + analyze button
if uploaded_file:
    image = Image.open(uploaded_file)
    st.session_state.uploaded_image = image

    img_col, btn_col = st.columns([1, 2])
    with img_col:
        st.image(image, caption="Your Product", use_container_width=True)
    with btn_col:
        st.markdown("### 🤖 AI Analysis Ready")
        st.markdown(f"**File:** {uploaded_file.name}")
        st.markdown(f"**Size:** {image.size[0]}×{image.size[1]}px")

        if not st.session_state.api_key:
            st.warning("⚠️ Please enter your Gemini API key in the sidebar first.")
        else:
            if st.button("🔍 Analyze Product (AI)", type="primary", use_container_width=True):
                with st.spinner("🤖 Gemini AI is analyzing your product... (5-10 seconds)"):
                    result = analyze_product_image(
                        image,
                        st.session_state.user_city,
                        st.session_state.user_state
                    )
                    st.session_state.analysis_result = result
                    if result.get("success"):
                        increment_analysis_count()
                        save_analysis(result, uploaded_file.name)
                        st.success("✅ Analysis complete! See results below in all 3 tabs.")
                        st.balloons()
                    else:
                        st.error(result.get("error", "Analysis failed. Please try again."))

# ─────────────────────────────────────────
# RESULTS — 3 TABS
# ─────────────────────────────────────────
result = st.session_state.analysis_result

if result and result.get("success"):
    product_category = result.get("category", "General")

    # Quick product summary
    st.markdown("---")
    st.markdown(f"""
    <div class="ai-result">
      <h3>🎯 {result.get('product_name', 'Your Product')}</h3>
      <p><b>Category:</b> {product_category} &nbsp;|&nbsp; <b>Sub-category:</b> {result.get('sub_category', '—')} &nbsp;|&nbsp; <b>Origin:</b> {result.get('origin_hint', 'Indian Craft')}</p>
      <p><b>Suggested Price:</b> ₹{result.get('price_suggestion', {}).get('min', 0)} – ₹{result.get('price_suggestion', {}).get('max', 0)}</p>
      <p><b>💡 Seller Tip:</b> {result.get('seller_tip', '')}</p>
    </div>
    """, unsafe_allow_html=True)

    # ─── 3 TABS ───
    tab1, tab2, tab3 = st.tabs([
        "🏆 Tab 1: Platform Intelligence",
        "📦 Tab 2: Bulk Suppliers & Contacts",
        "🚀 Tab 3: Seller & Buyer Registration"
    ])

    # ═══════════════════════════════════════
    # TAB 1: PLATFORM INTELLIGENCE
    # ═══════════════════════════════════════
    with tab1:
        st.markdown("## 🏆 Which Platform is Best for Your Product?")
        st.markdown(f"*Analysis for: **{result.get('product_name', 'Your Product')}** · Category: **{product_category}***")

        # Build platform comparison data
        platform_data = []
        for pname, pinfo in PLATFORMS.items():
            cat_data = pinfo["categories"].get(product_category, pinfo["categories"]["General"])
            platform_data.append({
                "Platform": pname,
                "Score": cat_data["score"],
                "Avg Rating": cat_data["avg_rating"],
                "Reviews": f"{cat_data['reviews']:,}",
                "Commission": f"{pinfo['commission']}%",
                "Price Range": f"₹{cat_data['price_range'][0]}–₹{cat_data['price_range'][1]}",
                "Est. Orders": cat_data["orders_range"],
                "logo": pinfo["logo"],
                "color": pinfo["color"],
                "signup_url": pinfo["signup_url"],
                "pros": pinfo["pros"],
                "cons": pinfo["cons"],
                "gst_required": pinfo["gst_required"],
            })

        # Sort by score
        platform_data.sort(key=lambda x: x["Score"], reverse=True)

        # ── Comparison Bar Chart ──
        fig = go.Figure()
        colors_list = [p["color"] for p in platform_data]
        fig.add_trace(go.Bar(
            x=[p["Platform"] for p in platform_data],
            y=[p["Score"] for p in platform_data],
            marker_color=colors_list,
            text=[f"{p['Score']}%" for p in platform_data],
            textposition="outside",
        ))
        fig.update_layout(
            title=f"Platform Match Score for '{product_category}'",
            yaxis_title="Match Score (%)",
            yaxis_range=[0, 100],
            showlegend=False,
            height=280,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Platform Cards ──
        for i, p in enumerate(platform_data):
            is_top = (i == 0)
            card_class = "platform-card top-pick" if is_top else "platform-card"

            col_logo, col_details, col_cta = st.columns([1, 3, 1.5])

            with col_logo:
                st.markdown(f"<div style='font-size:3rem;text-align:center;padding-top:1rem'>{p['logo']}</div>", unsafe_allow_html=True)
                if is_top:
                    st.markdown("<div style='text-align:center'><span class='badge-green'>🏅 BEST MATCH</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center;font-size:1.4rem;font-weight:700;color:{p['color']}'>{p['Score']}%</div>", unsafe_allow_html=True)

            with col_details:
                st.markdown(f"### {p['Platform']}")
                m1, m2, m3 = st.columns(3)
                m1.metric("⭐ Avg Rating", p["Avg Rating"])
                m2.metric("📝 Reviews", p["Reviews"])
                m3.metric("💸 Commission", p["Commission"])

                m4, m5 = st.columns(2)
                m4.metric("💰 Price Range", p["Price Range"])
                m5.metric("📦 Est. Orders", p["Est. Orders"])

                gst_badge = "⚠️ GST Required" if p["gst_required"] else "✅ No GST Needed"
                st.markdown(f"<span class='badge-{'orange' if p['gst_required'] else 'green'}'>{gst_badge}</span>", unsafe_allow_html=True)

                with st.expander("View Pros & Cons"):
                    pc1, pc2 = st.columns(2)
                    with pc1:
                        st.markdown("**✅ Pros:**")
                        for pro in p["pros"]:
                            st.markdown(f"• {pro}")
                    with pc2:
                        st.markdown("**❌ Cons:**")
                        for con in p["cons"]:
                            st.markdown(f"• {con}")

            with col_cta:
                st.markdown("<br>", unsafe_allow_html=True)
                st.link_button(
                    f"Register as Seller →",
                    p["signup_url"],
                    use_container_width=True,
                    type="primary" if is_top else "secondary"
                )
                st.markdown(f"<div style='font-size:0.75rem;color:#888;text-align:center;margin-top:4px'>Opens {p['Platform']} seller portal</div>", unsafe_allow_html=True)

            st.divider()

        # ── AI Listing Content ──
        st.markdown("### ✍️ Your AI-Generated Product Listing")
        list_col1, list_col2 = st.columns(2)
        with list_col1:
            st.markdown("**📋 Listing Title (copy-paste ready):**")
            st.code(result.get("listing_title", ""), language=None)

            st.markdown("**🏷️ SEO Tags:**")
            tags = result.get("seo_tags", [])
            st.code(", ".join(tags), language=None)

        with list_col2:
            st.markdown("**📝 Product Description:**")
            st.text_area("", value=result.get("listing_description", ""), height=200, label_visibility="collapsed")

        # USPs
        st.markdown("**🌟 Unique Selling Points:**")
        usps = result.get("unique_selling_points", [])
        usp_cols = st.columns(len(usps) if usps else 1)
        for i, usp in enumerate(usps):
            usp_cols[i].markdown(f"<div class='step-box'>🎯 {usp}</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # TAB 2: BULK SUPPLIERS & CONTACTS
    # ═══════════════════════════════════════
    with tab2:
        st.markdown("## 📦 Raw Material Suppliers & Bulk Contacts")

        user_city = st.session_state.user_city
        user_state = st.session_state.user_state

        location_display = f"{user_city}, {user_state}" if user_city or user_state else "All India"
        st.markdown(f"*Showing suppliers for: **{product_category}** · Location: **{location_display}***")

        # Location override
        loc_override = st.text_input("🔍 Search suppliers in a different city:", placeholder="Type city name...", key="loc_search")
        search_city = loc_override.lower() if loc_override else user_city.lower()

        # Get suppliers for this category
        suppliers = SUPPLIERS_DB.get(product_category, SUPPLIERS_DB.get("General", []))
        all_suppliers = SUPPLIERS_DB.get("General", [])

        # Filter by location if provided
        filtered_suppliers = suppliers
        if search_city and search_city.strip():
            filtered_suppliers = [s for s in suppliers if search_city in s["city"].lower() or search_city in s["state"].lower()]
            if not filtered_suppliers:
                st.info(f"No local suppliers found for '{search_city}'. Showing all India suppliers.")
                filtered_suppliers = suppliers

        if not filtered_suppliers:
            filtered_suppliers = all_suppliers

        # Supplier count summary
        verified_count = sum(1 for s in filtered_suppliers if s["verified"])
        st.markdown(f"Found **{len(filtered_suppliers)} suppliers** · {verified_count} verified ✅")
        st.divider()

        # ── Supplier Cards ──
        for s in filtered_suppliers:
            verified_class = "verified" if s["verified"] else "unverified"
            verified_label = "✅ Verified Supplier" if s["verified"] else "⚠️ Unverified (Call to confirm)"

            with st.container():
                col_info, col_moq, col_contact = st.columns([2.5, 1.5, 1.5])

                with col_info:
                    st.markdown(f"#### 🏭 {s['name']}")
                    st.markdown(f"📍 **{s['city']}, {s['state']}**")
                    st.markdown(f"🔧 **Supplies:** {s['type']}")
                    badge_color = "green" if s["verified"] else "orange"
                    st.markdown(f"<span class='badge-{badge_color}'>{verified_label}</span>", unsafe_allow_html=True)

                with col_moq:
                    st.markdown("**📦 MOQ Details:**")
                    st.markdown(f"Min Order: **{s['moq']}**")
                    st.markdown(f"Price: **{s['price']}**")

                with col_contact:
                    st.markdown("**📱 Contact:**")
                    wa_url = f"https://wa.me/{s['whatsapp']}?text=Hi%2C+I+am+a+small+seller+looking+for+{product_category.replace(' ', '+')}+in+bulk.+Can+you+share+MOQ+and+price+details%3F"
                    st.link_button("💬 WhatsApp", wa_url, use_container_width=True)
                    st.link_button("🗺️ View on Map", s["maps_url"], use_container_width=True)

                st.divider()

        # ── Additional B2B Platforms ──
        st.markdown("### 🌐 Also Search on These Platforms")
        b2b_col1, b2b_col2, b2b_col3 = st.columns(3)

        with b2b_col1:
            st.markdown("""
            <div class="step-box">
              <b>🇮🇳 IndiaMART</b><br><br>
              India's largest B2B marketplace<br>
              10M+ verified suppliers
            </div>
            """, unsafe_allow_html=True)
            st.link_button("Search IndiaMART", f"https://www.indiamart.com/search.mp?ss={product_category.replace(' ', '+')}", use_container_width=True)

        with b2b_col2:
            st.markdown("""
            <div class="step-box">
              <b>🔄 TradeIndia</b><br><br>
              Pan-India wholesale directory<br>
              3M+ suppliers listed
            </div>
            """, unsafe_allow_html=True)
            st.link_button("Search TradeIndia", f"https://www.tradeindia.com/Wholesale/{product_category.replace(' ', '-')}.html", use_container_width=True)

        with b2b_col3:
            st.markdown("""
            <div class="step-box">
              <b>🏛️ MSME Directory</b><br><br>
              Govt-verified artisan clusters<br>
              GI-tagged craft districts
            </div>
            """, unsafe_allow_html=True)
            st.link_button("MSME Clusters", "https://msme.gov.in/1-industrial-clusters", use_container_width=True)

        # ── WhatsApp message template ──
        st.markdown("### 📋 Ready-to-Send WhatsApp Message Template")
        wa_template = f"""Hi,

I am a small handmade product seller looking for bulk raw materials for {product_category}.

Product: {result.get('product_name', 'Handmade product')}
Materials needed: {', '.join(result.get('materials', ['raw materials']))}

Please share:
• MOQ (minimum order quantity)
• Price per unit/meter/kg
• Payment terms
• Delivery time to {location_display}

Thank you!"""
        st.text_area("Copy this message:", value=wa_template, height=200)

    # ═══════════════════════════════════════
    # TAB 3: SELLER & BUYER REGISTRATION
    # ═══════════════════════════════════════
    with tab3:
        st.markdown("## 🚀 One-Click Business Setup")

        reg_tab1, reg_tab2, reg_tab3 = st.tabs(["📋 Document Checklist", "👤 Register as Seller", "🛒 Register as Buyer"])

        # ── Document Checklist ──
        with reg_tab1:
            st.markdown("### 📋 What You Need to Start Selling")
            st.markdown(f"*For your product: **{result.get('product_name', '')}***")
            st.markdown("")

            for doc in SELLER_DOCS:
                col_check, col_doc, col_note = st.columns([0.5, 2, 3])
                with col_check:
                    checked = st.checkbox("", key=f"doc_{doc['doc']}", value=False)
                with col_doc:
                    req_label = "🔴 Required" if doc["required"] else "🟡 Optional"
                    st.markdown(f"**{doc['doc']}**")
                    st.markdown(f"<span class='badge-{'orange' if doc['required'] else 'blue'}'>{req_label}</span>", unsafe_allow_html=True)
                with col_note:
                    st.markdown(f"*{doc['note']}*")
                    platforms_str = " · ".join(doc["platforms"])
                    st.markdown(f"<small>Needed for: {platforms_str}</small>", unsafe_allow_html=True)
                st.divider()

            st.markdown("### 🔗 Direct Platform Registration Links")
            p_col1, p_col2, p_col3 = st.columns(3)
            with p_col1:
                st.markdown("**🛍️ Meesho**")
                st.markdown("No GST · No listing fee")
                st.link_button("Register on Meesho →", "https://supplier.meesho.com", use_container_width=True, type="primary")
            with p_col2:
                st.markdown("**⭐ Flipkart**")
                st.markdown("Ekart logistics · PAN needed")
                st.link_button("Register on Flipkart →", "https://seller.flipkart.com", use_container_width=True)
            with p_col3:
                st.markdown("**📦 Amazon India**")
                st.markdown("GST preferred · FBA available")
                st.link_button("Register on Amazon →", "https://sell.amazon.in", use_container_width=True)

            # MSME scheme
            st.markdown("---")
            st.markdown("### 🏛️ Government Schemes for Small Sellers")
            gov_col1, gov_col2 = st.columns(2)
            with gov_col1:
                st.markdown("""
                **📜 Udyam Registration (Free MSME)**
                - Free government MSME certificate
                - Priority loans at lower interest
                - Government scheme access
                """)
                st.link_button("Register for Udyam →", "https://udyamregistration.gov.in", use_container_width=True)
            with gov_col2:
                st.markdown("""
                **🎨 GI Tag & Craft Board**
                - Protect your craft's geographical origin
                - Premium pricing recognition
                - Export market access
                """)
                st.link_button("Explore Craft Board →", "https://www.craftcouncilofindia.org", use_container_width=True)

        # ── Seller Registration ──
        with reg_tab2:
            st.markdown("### 👤 Create Your CarryMe Seller Account")
            st.markdown("*Save your analyses, track products, get personalized insights*")
            st.markdown("")

            with st.form("seller_registration"):
                s_col1, s_col2 = st.columns(2)
                with s_col1:
                    s_name = st.text_input("Full Name *", placeholder="e.g., Priya Sharma")
                    s_phone = st.text_input("Mobile Number *", placeholder="e.g., 9876543210")
                    s_city = st.text_input("City / District *", placeholder="e.g., Surat", value=st.session_state.user_city)
                with s_col2:
                    s_state = st.selectbox("State *", ["Select State"] + INDIAN_STATES)
                    s_category = st.selectbox("Main Product Category *", list(PLATFORMS["Meesho"]["categories"].keys()))
                    s_platform = st.multiselect("Platforms you want to sell on:", ["Meesho", "Flipkart", "Amazon India"], default=["Meesho"])

                s_product = st.text_input("Your Current Product", placeholder=result.get('product_name', 'e.g., Handmade Dupatta'), value=result.get('product_name', ''))
                s_business = st.text_input("Business/Store Name (optional)", placeholder="e.g., Priya Crafts")
                s_experience = st.radio("Selling Experience:", ["New seller (just starting)", "1-2 years", "3+ years"], horizontal=True)
                s_agree = st.checkbox("I agree to CarryMe Store terms and privacy policy")

                submitted = st.form_submit_button("🚀 Create Seller Account", type="primary", use_container_width=True)

                if submitted:
                    if not s_name or not s_phone or s_state == "Select State":
                        st.error("Please fill all required fields (marked with *)")
                    elif not s_agree:
                        st.warning("Please agree to the terms to continue.")
                    else:
                        seller_data = {
                            "name": s_name, "phone": s_phone, "city": s_city,
                            "state": s_state, "category": s_category,
                            "platforms": s_platform, "product": s_product,
                            "business_name": s_business or f"{s_name} Crafts",
                            "experience": s_experience
                        }
                        register_user("seller", seller_data)
                        st.success(f"🎉 Welcome to CarryMe, {s_name}! Your seller ID: {seller_data.get('id', 'S1001')}")
                        st.balloons()
                        st.markdown(f"""
                        <div class="ai-result">
                          <h4>✅ Account Created Successfully!</h4>
                          <b>Seller ID:</b> {seller_data.get('id', 'S1001')}<br>
                          <b>Business:</b> {seller_data.get('business_name')}<br>
                          <b>Category:</b> {s_category}<br>
                          <b>Recommended Platform:</b> {s_platform[0] if s_platform else 'Meesho'}<br><br>
                          <b>Next Step:</b> Register on {s_platform[0] if s_platform else 'Meesho'} using the links in the Document Checklist tab.
                        </div>
                        """, unsafe_allow_html=True)

        # ── Buyer Registration ──
        with reg_tab3:
            st.markdown("### 🛒 Register as an End User / Buyer")
            st.markdown("*Discover handmade Indian products · Contact sellers directly*")
            st.markdown("")

            with st.form("buyer_registration"):
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    b_name = st.text_input("Full Name *", placeholder="e.g., Rahul Kumar")
                    b_phone = st.text_input("Mobile Number *", placeholder="e.g., 9876543210")
                    b_city = st.text_input("Your City *", placeholder="e.g., Mumbai")
                with b_col2:
                    b_state = st.selectbox("State *", ["Select State"] + INDIAN_STATES, key="buyer_state")
                    b_interest = st.multiselect("Interested Product Categories:", list(PLATFORMS["Meesho"]["categories"].keys()))
                    b_budget = st.select_slider("Typical Budget per Item (₹):", options=[50, 100, 200, 500, 1000, 2000, 5000], value=500)

                b_purpose = st.radio("Buying for:", ["Personal use", "Gift", "Resale/Business", "Interior decoration"], horizontal=True)
                b_agree = st.checkbox("I agree to CarryMe Store buyer terms")

                b_submitted = st.form_submit_button("🛒 Create Buyer Account", type="primary", use_container_width=True)

                if b_submitted:
                    if not b_name or not b_phone or b_state == "Select State":
                        st.error("Please fill all required fields (marked with *)")
                    elif not b_agree:
                        st.warning("Please agree to the terms to continue.")
                    else:
                        buyer_data = {
                            "name": b_name, "phone": b_phone, "city": b_city,
                            "state": b_state, "interests": b_interest,
                            "budget": b_budget, "purpose": b_purpose
                        }
                        register_user("buyer", buyer_data)
                        st.success(f"🎉 Welcome to CarryMe, {b_name}! Your buyer ID: {buyer_data.get('id', 'B1001')}")
                        st.markdown(f"""
                        <div class="ai-result">
                          <h4>✅ Buyer Account Created!</h4>
                          <b>Buyer ID:</b> {buyer_data.get('id', 'B1001')}<br>
                          <b>Location:</b> {b_city}, {b_state}<br>
                          <b>Budget:</b> up to ₹{b_budget} per item<br>
                          <b>Interests:</b> {', '.join(b_interest) if b_interest else 'All categories'}<br><br>
                          You can now connect directly with verified Indian handmade sellers!
                        </div>
                        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# EMPTY STATE (no image uploaded)
# ─────────────────────────────────────────
elif not uploaded_file:
    st.markdown("---")
    st.markdown("### 🌟 How CarryMe Store Works")

    how_col1, how_col2, how_col3 = st.columns(3)
    with how_col1:
        st.markdown("""
        <div class="step-box">
          <div style="font-size:2.5rem">📸</div>
          <h4>Step 1: Upload Photo</h4>
          <p>Click or upload your handmade product photo. No studio needed — good natural light works!</p>
        </div>
        """, unsafe_allow_html=True)
    with how_col2:
        st.markdown("""
        <div class="step-box">
          <div style="font-size:2.5rem">🤖</div>
          <h4>Step 2: AI Analysis</h4>
          <p>Gemini AI identifies your product, generates SEO listing, and finds the best platform match.</p>
        </div>
        """, unsafe_allow_html=True)
    with how_col3:
        st.markdown("""
        <div class="step-box">
          <div style="font-size:2.5rem">🚀</div>
          <h4>Step 3: Go Live!</h4>
          <p>Get platform ratings, contact bulk suppliers, and register your seller account — all in one click.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Platform Quick Stats")
    stats_df = pd.DataFrame([
        {"Platform": "Meesho 🛍️", "Commission": "1.8%", "GST Needed": "No", "Best For": "High volume ethnic goods", "Reach": "Tier 2/3/4 cities"},
        {"Platform": "Flipkart ⭐", "Commission": "8.5%", "GST Needed": "No*", "Best For": "Mid-range branded look", "Reach": "Pan India"},
        {"Platform": "Amazon India 📦", "Commission": "10%", "GST Needed": "Preferred", "Best For": "Premium & export", "Reach": "Premium urban buyers"},
    ])
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="info-box">
      💡 <b>Tip:</b> Start with <b>Meesho</b> — lowest commission (1.8%), no GST required, and the largest Tier 3/4 buyer base in India.
      Once you have 20+ reviews, expand to Flipkart and Amazon.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#888;font-size:0.85rem;padding:1rem">
  🛍️ <b>CarryMe Store</b> · AI-Powered Seller Intelligence for Indian Handmade Products<br>
  Built with ❤️ for Tier 3 & 4 India · Powered by Google Gemini AI (Free) · Deployed on Streamlit Cloud<br>
  <small>Not affiliated with Meesho, Flipkart or Amazon. Data is indicative and updated periodically.</small>
</div>
""", unsafe_allow_html=True)
