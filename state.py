# state.py — Session State Management
import streamlit as st
import json
from datetime import datetime


def init_state():
    """Initialize all session state variables."""
    defaults = {
        "api_key": "",
        "api_key_verified": False,
        "analysis_result": None,
        "uploaded_image": None,
        "user_city": "",
        "user_state": "",
        "analysis_count": 0,
        "registered_sellers": [],
        "registered_buyers": [],
        "products_history": [],
        "active_tab": 0,
        "show_registration": False,
        "reg_type": "seller",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def save_analysis(result: dict, image_name: str = "product"):
    """Save analysis to history."""
    if result and result.get("success"):
        entry = {
            "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
            "product_name": result.get("product_name", "Unknown"),
            "category": result.get("category", "General"),
            "image_name": image_name,
            "platform_rec": result.get("platform_recommendation", "Meesho"),
        }
        st.session_state.products_history.append(entry)
        if len(st.session_state.products_history) > 20:
            st.session_state.products_history = st.session_state.products_history[-20:]


def register_user(user_type: str, data: dict) -> bool:
    """Register a new seller or buyer."""
    data["registered_at"] = datetime.now().strftime("%d %b %Y, %H:%M")
    data["id"] = f"{user_type[0].upper()}{len(st.session_state.get(f'registered_{user_type}s', [])) + 1001}"

    if user_type == "seller":
        st.session_state.registered_sellers.append(data)
    else:
        st.session_state.registered_buyers.append(data)
    return True


def get_analysis_count() -> int:
    return st.session_state.get("analysis_count", 0)


def increment_analysis_count():
    st.session_state.analysis_count = st.session_state.get("analysis_count", 0) + 1
