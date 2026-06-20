# config.py — CarryMe Store Configuration
# All platform data, categories, and supplier seed data

APP_NAME = "CarryMe Store"
APP_TAGLINE = "One Photo → Instant Business Intelligence for Indian Sellers"
VERSION = "1.0.0"

# ─────────────────────────────────────────
# PLATFORM INTELLIGENCE DATA
# ─────────────────────────────────────────
PLATFORMS = {
    "Meesho": {
        "logo": "🛍️",
        "color": "#9B2C8D",
        "signup_url": "https://supplier.meesho.com",
        "commission": 1.8,
        "categories": {
            "Fashion & Apparel": {"avg_rating": 4.3, "reviews": 189420, "price_range": (80, 650), "orders_range": "500–2000/mo", "score": 95},
            "Ethnic Wear": {"avg_rating": 4.4, "reviews": 142000, "price_range": (100, 800), "orders_range": "400–1800/mo", "score": 96},
            "Handmade Jewelry": {"avg_rating": 4.2, "reviews": 98000, "price_range": (50, 500), "orders_range": "300–1200/mo", "score": 90},
            "Home Decor": {"avg_rating": 4.1, "reviews": 76000, "price_range": (80, 900), "orders_range": "200–800/mo", "score": 85},
            "Handicrafts": {"avg_rating": 4.3, "reviews": 54000, "price_range": (100, 1200), "orders_range": "150–600/mo", "score": 88},
            "Bags & Accessories": {"avg_rating": 4.2, "reviews": 112000, "price_range": (60, 700), "orders_range": "250–1000/mo", "score": 87},
            "Toys & Kids": {"avg_rating": 4.0, "reviews": 43000, "price_range": (50, 400), "orders_range": "100–400/mo", "score": 80},
            "Candles & Aroma": {"avg_rating": 4.4, "reviews": 31000, "price_range": (80, 500), "orders_range": "100–350/mo", "score": 83},
            "Paintings & Art": {"avg_rating": 4.5, "reviews": 21000, "price_range": (200, 5000), "orders_range": "30–120/mo", "score": 78},
            "General": {"avg_rating": 4.1, "reviews": 89000, "price_range": (50, 600), "orders_range": "200–700/mo", "score": 82},
        },
        "pros": ["Lowest commission (1.8%)", "Tier 2/3/4 city reach", "No listing fee", "Hindi support"],
        "cons": ["Lower price realization", "High competition volume"],
        "gst_required": False,
        "min_price": 50,
    },
    "Flipkart": {
        "logo": "⭐",
        "color": "#2874F0",
        "signup_url": "https://seller.flipkart.com",
        "commission": 8.5,
        "categories": {
            "Fashion & Apparel": {"avg_rating": 4.1, "reviews": 98000, "price_range": (150, 1200), "orders_range": "100–500/mo", "score": 80},
            "Ethnic Wear": {"avg_rating": 4.2, "reviews": 76000, "price_range": (200, 1500), "orders_range": "80–400/mo", "score": 82},
            "Handmade Jewelry": {"avg_rating": 4.0, "reviews": 54000, "price_range": (100, 800), "orders_range": "60–250/mo", "score": 75},
            "Home Decor": {"avg_rating": 4.2, "reviews": 89000, "price_range": (150, 2000), "orders_range": "80–350/mo", "score": 83},
            "Handicrafts": {"avg_rating": 4.1, "reviews": 32000, "price_range": (150, 2000), "orders_range": "40–180/mo", "score": 76},
            "Bags & Accessories": {"avg_rating": 4.0, "reviews": 67000, "price_range": (100, 1200), "orders_range": "70–300/mo", "score": 77},
            "Toys & Kids": {"avg_rating": 4.2, "reviews": 98000, "price_range": (80, 800), "orders_range": "80–400/mo", "score": 82},
            "Candles & Aroma": {"avg_rating": 4.1, "reviews": 18000, "price_range": (100, 800), "orders_range": "40–160/mo", "score": 72},
            "Paintings & Art": {"avg_rating": 4.3, "reviews": 12000, "price_range": (300, 8000), "orders_range": "15–60/mo", "score": 70},
            "General": {"avg_rating": 4.0, "reviews": 54000, "price_range": (100, 1000), "orders_range": "60–250/mo", "score": 74},
        },
        "pros": ["Faster logistics (Ekart)", "Better brand recognition", "Flipkart Assured badge"],
        "cons": ["8.5% commission", "Strict quality checks", "GST required above ₹40L"],
        "gst_required": False,
        "min_price": 100,
    },
    "Amazon India": {
        "logo": "📦",
        "color": "#FF9900",
        "signup_url": "https://sell.amazon.in",
        "commission": 10.0,
        "categories": {
            "Fashion & Apparel": {"avg_rating": 4.0, "reviews": 76000, "price_range": (200, 2000), "orders_range": "30–150/mo", "score": 72},
            "Ethnic Wear": {"avg_rating": 4.1, "reviews": 54000, "price_range": (250, 2500), "orders_range": "25–120/mo", "score": 73},
            "Handmade Jewelry": {"avg_rating": 4.2, "reviews": 43000, "price_range": (150, 1500), "orders_range": "20–80/mo", "score": 74},
            "Home Decor": {"avg_rating": 4.3, "reviews": 98000, "price_range": (200, 5000), "orders_range": "30–120/mo", "score": 76},
            "Handicrafts": {"avg_rating": 4.4, "reviews": 28000, "price_range": (200, 3000), "orders_range": "20–80/mo", "score": 78},
            "Bags & Accessories": {"avg_rating": 4.1, "reviews": 54000, "price_range": (150, 2000), "orders_range": "25–100/mo", "score": 72},
            "Toys & Kids": {"avg_rating": 4.3, "reviews": 120000, "price_range": (100, 1500), "orders_range": "30–150/mo", "score": 75},
            "Candles & Aroma": {"avg_rating": 4.4, "reviews": 23000, "price_range": (150, 1200), "orders_range": "20–80/mo", "score": 73},
            "Paintings & Art": {"avg_rating": 4.5, "reviews": 9000, "price_range": (500, 15000), "orders_range": "5–30/mo", "score": 71},
            "General": {"avg_rating": 4.1, "reviews": 43000, "price_range": (150, 1500), "orders_range": "20–80/mo", "score": 70},
        },
        "pros": ["Global export potential", "FBA logistics", "Premium buyer segment", "Amazon Launchpad for handmade"],
        "cons": ["10% commission", "Strict returns policy", "Higher price expectation"],
        "gst_required": True,
        "min_price": 150,
    },
}

# ─────────────────────────────────────────
# SUPPLIER SEED DATABASE
# ─────────────────────────────────────────
SUPPLIERS_DB = {
    "Fashion & Apparel": [
        {"name": "Surat Textile Market", "city": "Surat", "state": "Gujarat", "type": "Wholesale Fabric", "moq": "10 meters", "price": "₹40–120/meter", "whatsapp": "919825001001", "maps_url": "https://maps.google.com/?q=Surat+Textile+Market", "verified": True},
        {"name": "Chandni Chowk Wholesale Hub", "city": "Delhi", "state": "Delhi", "type": "Fabric & Thread", "moq": "5 meters", "price": "₹35–200/meter", "whatsapp": "919811001001", "maps_url": "https://maps.google.com/?q=Chandni+Chowk+Delhi", "verified": True},
        {"name": "Dharavi Leather Cluster", "city": "Mumbai", "state": "Maharashtra", "type": "Leather & Accessories", "moq": "20 pieces", "price": "₹80–300/piece", "whatsapp": "919820001001", "maps_url": "https://maps.google.com/?q=Dharavi+Mumbai", "verified": True},
        {"name": "Tirupur Knitting Mills", "city": "Tirupur", "state": "Tamil Nadu", "type": "Knitwear Fabric", "moq": "50 kg", "price": "₹180–350/kg", "whatsapp": "919843001001", "maps_url": "https://maps.google.com/?q=Tirupur+Tamil+Nadu", "verified": True},
    ],
    "Ethnic Wear": [
        {"name": "Jaipur Bandhej Suppliers", "city": "Jaipur", "state": "Rajasthan", "type": "Ethnic Fabric & Dye", "moq": "20 meters", "price": "₹60–250/meter", "whatsapp": "919829001001", "maps_url": "https://maps.google.com/?q=Jaipur+Textile+Market", "verified": True},
        {"name": "Varanasi Silk House", "city": "Varanasi", "state": "UP", "type": "Silk & Brocade", "moq": "5 meters", "price": "₹400–2000/meter", "whatsapp": "919415001001", "maps_url": "https://maps.google.com/?q=Varanasi+Silk+Market", "verified": True},
        {"name": "Lucknow Chikankari Cluster", "city": "Lucknow", "state": "UP", "type": "Embroidery & Chikan", "moq": "10 pieces", "price": "₹150–600/piece", "whatsapp": "919889001001", "maps_url": "https://maps.google.com/?q=Lucknow+Chikankari", "verified": False},
        {"name": "Kanchipuram Weavers Co-op", "city": "Kanchipuram", "state": "Tamil Nadu", "type": "Silk Sarees Raw Material", "moq": "3 meters", "price": "₹800–3500/meter", "whatsapp": "919842001001", "maps_url": "https://maps.google.com/?q=Kanchipuram", "verified": True},
    ],
    "Handmade Jewelry": [
        {"name": "Rajkot Imitation Wholesale", "city": "Rajkot", "state": "Gujarat", "type": "Imitation Jewelry Parts", "moq": "100 pieces", "price": "₹5–80/piece", "whatsapp": "919824001001", "maps_url": "https://maps.google.com/?q=Rajkot+Jewelry+Market", "verified": True},
        {"name": "Jaipur Gems & Beads", "city": "Jaipur", "state": "Rajasthan", "type": "Semi-precious Stones & Beads", "moq": "50 grams", "price": "₹40–800/gram", "whatsapp": "919828001001", "maps_url": "https://maps.google.com/?q=Jaipur+Gems+Market", "verified": True},
        {"name": "Mumbai Zaveri Bazaar", "city": "Mumbai", "state": "Maharashtra", "type": "Gold & Silver Findings", "moq": "10 grams", "price": "₹5500–7000/gram gold", "whatsapp": "919821001001", "maps_url": "https://maps.google.com/?q=Zaveri+Bazaar+Mumbai", "verified": True},
        {"name": "Moradabad Brass Parts", "city": "Moradabad", "state": "UP", "type": "Brass Jewelry Components", "moq": "500 pieces", "price": "₹2–25/piece", "whatsapp": "919411001001", "maps_url": "https://maps.google.com/?q=Moradabad+Brass+Market", "verified": False},
    ],
    "Home Decor": [
        {"name": "Moradabad Handicraft Export Zone", "city": "Moradabad", "state": "UP", "type": "Brass & Metal Decor", "moq": "20 pieces", "price": "₹50–500/piece", "whatsapp": "919412001001", "maps_url": "https://maps.google.com/?q=Moradabad+Handicraft", "verified": True},
        {"name": "Saharanpur Wood Craft Market", "city": "Saharanpur", "state": "UP", "type": "Wood Carving Blanks", "moq": "10 pieces", "price": "₹30–800/piece", "whatsapp": "919927001001", "maps_url": "https://maps.google.com/?q=Saharanpur+Wood+Market", "verified": True},
        {"name": "Khurja Pottery Cluster", "city": "Khurja", "state": "UP", "type": "Ceramic & Pottery Raw", "moq": "50 pieces", "price": "₹15–200/piece", "whatsapp": "919457001001", "maps_url": "https://maps.google.com/?q=Khurja+Pottery", "verified": False},
        {"name": "Jodhpur Furniture & Decor", "city": "Jodhpur", "state": "Rajasthan", "type": "Furniture & Decor Parts", "moq": "5 pieces", "price": "₹200–2000/piece", "whatsapp": "919829501001", "maps_url": "https://maps.google.com/?q=Jodhpur+Furniture+Market", "verified": True},
    ],
    "Handicrafts": [
        {"name": "Kutch Craft Cooperative", "city": "Bhuj", "state": "Gujarat", "type": "Raw Material & Tools", "moq": "1 kit", "price": "₹300–2000/kit", "whatsapp": "919824501001", "maps_url": "https://maps.google.com/?q=Bhuj+Gujarat+Craft", "verified": True},
        {"name": "Kondapalli Toy Makers", "city": "Vijayawada", "state": "Andhra Pradesh", "type": "Wood Toy Parts", "moq": "25 pieces", "price": "₹20–150/piece", "whatsapp": "919849001001", "maps_url": "https://maps.google.com/?q=Kondapalli+Andhra", "verified": True},
        {"name": "Channapatna Lacquer Craft", "city": "Channapatna", "state": "Karnataka", "type": "Lacquer & Toy Wood", "moq": "10 pieces", "price": "₹30–200/piece", "whatsapp": "919845001001", "maps_url": "https://maps.google.com/?q=Channapatna+Karnataka", "verified": False},
        {"name": "Bastar Iron Craft Cluster", "city": "Jagdalpur", "state": "Chhattisgarh", "type": "Tribal Art Supplies", "moq": "5 kg", "price": "₹80–300/kg", "whatsapp": "919827001001", "maps_url": "https://maps.google.com/?q=Jagdalpur+Chhattisgarh", "verified": True},
    ],
    "Bags & Accessories": [
        {"name": "Kolkata Bag Wholesale Market", "city": "Kolkata", "state": "West Bengal", "type": "Jute & Canvas Bags", "moq": "50 pieces", "price": "₹25–200/piece", "whatsapp": "919830001001", "maps_url": "https://maps.google.com/?q=Kolkata+Bag+Market", "verified": True},
        {"name": "Chennai Leather Goods Cluster", "city": "Chennai", "state": "Tamil Nadu", "type": "Leather Cuts & Zippers", "moq": "20 pieces", "price": "₹40–400/piece", "whatsapp": "919841001001", "maps_url": "https://maps.google.com/?q=Chennai+Leather+Market", "verified": True},
        {"name": "Agra Leather Zone", "city": "Agra", "state": "UP", "type": "Leather Sheets & Hardware", "moq": "5 sq meters", "price": "₹200–800/sq meter", "whatsapp": "919719001001", "maps_url": "https://maps.google.com/?q=Agra+Leather+Zone", "verified": False},
    ],
    "Candles & Aroma": [
        {"name": "Mumbai Fragrance Wholesale", "city": "Mumbai", "state": "Maharashtra", "type": "Wax, Wicks & Fragrances", "moq": "5 kg", "price": "₹120–400/kg", "whatsapp": "919022001001", "maps_url": "https://maps.google.com/?q=Mumbai+Chemical+Market", "verified": True},
        {"name": "Kannauj Attar Market", "city": "Kannauj", "state": "UP", "type": "Essential Oils & Attar", "moq": "100 ml", "price": "₹200–5000/100ml", "whatsapp": "919795001001", "maps_url": "https://maps.google.com/?q=Kannauj+UP+Perfume", "verified": True},
        {"name": "Bangalore Craft Supplies", "city": "Bengaluru", "state": "Karnataka", "type": "Candle Molds & Dyes", "moq": "1 set", "price": "₹150–800/set", "whatsapp": "919880001001", "maps_url": "https://maps.google.com/?q=Bangalore+Craft+Store", "verified": False},
    ],
    "Paintings & Art": [
        {"name": "Delhi Art Supplies Hub", "city": "Delhi", "state": "Delhi", "type": "Canvas, Colors & Brushes", "moq": "1 kit", "price": "₹200–2000/kit", "whatsapp": "919810001001", "maps_url": "https://maps.google.com/?q=Delhi+Art+Market+Connaught", "verified": True},
        {"name": "Jaipur Miniature Art Suppliers", "city": "Jaipur", "state": "Rajasthan", "type": "Natural Pigments & Parchment", "moq": "500 grams", "price": "₹100–800/100grams", "whatsapp": "919832001001", "maps_url": "https://maps.google.com/?q=Jaipur+Art+Supplies", "verified": False},
        {"name": "Thane Art Materials", "city": "Thane", "state": "Maharashtra", "type": "Acrylic, Oil & Watercolor", "moq": "1 set", "price": "₹300–1500/set", "whatsapp": "919821501001", "maps_url": "https://maps.google.com/?q=Thane+Art+Supply", "verified": True},
    ],
    "Toys & Kids": [
        {"name": "Sivakasi Toy Raw Material", "city": "Sivakasi", "state": "Tamil Nadu", "type": "Plastic Parts & Molds", "moq": "100 pieces", "price": "₹5–50/piece", "whatsapp": "919842501001", "maps_url": "https://maps.google.com/?q=Sivakasi+Tamil+Nadu", "verified": True},
        {"name": "Alibaba India (B2B Direct)", "city": "Pan India", "state": "All India", "type": "All Toy Components", "moq": "50 pieces", "price": "₹10–200/piece", "whatsapp": "918000001001", "maps_url": "https://maps.google.com/?q=India+Toy+Market", "verified": False},
    ],
    "General": [
        {"name": "IndiaMART Verified Suppliers", "city": "Pan India", "state": "All India", "type": "All Categories", "moq": "Varies", "price": "Negotiable", "whatsapp": "918888001001", "maps_url": "https://www.indiamart.com", "verified": True},
        {"name": "TradeIndia Bulk Suppliers", "city": "Pan India", "state": "All India", "type": "All Categories", "moq": "Varies", "price": "Negotiable", "whatsapp": "917777001001", "maps_url": "https://www.tradeindia.com", "verified": True},
    ],
}

# Document checklist for seller registration
SELLER_DOCS = [
    {"doc": "Aadhaar Card", "required": True, "platforms": ["Meesho", "Flipkart", "Amazon India"], "note": "Primary identity proof"},
    {"doc": "PAN Card", "required": True, "platforms": ["Flipkart", "Amazon India"], "note": "Required for tax purposes"},
    {"doc": "Bank Account + IFSC", "required": True, "platforms": ["Meesho", "Flipkart", "Amazon India"], "note": "For payment settlements"},
    {"doc": "GST Number", "required": False, "platforms": ["Amazon India"], "note": "Only needed for Amazon India if turnover > ₹40L. Optional for Meesho/Flipkart"},
    {"doc": "MSME/Udyam Certificate", "required": False, "platforms": ["Meesho", "Flipkart", "Amazon India"], "note": "Unlocks government subsidies & priority support"},
    {"doc": "Cancel Cheque / Passbook Copy", "required": True, "platforms": ["Meesho", "Flipkart", "Amazon India"], "note": "Bank account verification"},
    {"doc": "Product Photos (plain background)", "required": True, "platforms": ["Meesho", "Flipkart", "Amazon India"], "note": "Min 3 photos per product, 500x500px+"},
]

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu & Kashmir", "Ladakh", "Puducherry", "Chandigarh"
]
