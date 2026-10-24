import streamlit as st
from frontend.components.header_banner import render_header_banner
from frontend.components.alert_box import render_coastal_alerts_view
from frontend.services.api import get_latest_conditions
from frontend.services.prediction_service import get_active_alerts
from frontend.config.config import STATION_KEY_TO_NAME
from backend.database.db import get_recent_alert_logs

def render_alerts_page():
    station_key = st.session_state.get("selected_station", "chennai")
    station_name = STATION_KEY_TO_NAME.get(station_key, "Chennai Coast")
    last_updated = st.session_state.get("last_updated", "2:29 PM")
    
    # 1. Header Banner
    render_header_banner(
        icon="🚨",
        title="Coastal Alerts & Advisories",
        subtitle="Active Metocean Risk Warnings and Historical Hazard Log",
        station_name=station_name,
        last_updated=last_updated,
        refresh_button_label="Refresh Alerts",
        station_key=station_key
    )
    
    # Fetch current observations & alert status
    conditions = get_latest_conditions(station_key)
    alert_info = get_active_alerts(conditions)
    
    # 2. Hero Alert Status & Operational Maritime Recommendations (Matching Reference Image 2)
    render_coastal_alerts_view(alert_info)
    
    # 3. Advisory Threshold Cheat Sheet
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
    with st.expander("📖 Marine Classification Benchmarks & Safety Guidelines", expanded=False):
        st.markdown("""
        | Severity Level | Significant Wave Height ($H_s$) | Risk Score | Operational Directive |
        | :--- | :--- | :--- | :--- |
        | 🟢 **CALM** | $< 1.5\\text{ m}$ | $0 - 35$ | Safe for all recreational and artisanal fishing activities. |
        | 🟡 **MODERATE** | $1.5\\text{ m} - 2.5\\text{ m}$ | $36 - 65$ | Noticeable swell. Small craft advisory recommended. |
        | 🟠 **ROUGH** | $2.5\\text{ m} - 3.5\\text{ m}$ | $66 - 85$ | High wave energy. Artisanal craft restriction; harbor surge warning. |
        | 🔴 **VERY ROUGH** | $> 3.5\\text{ m}$ | $86 - 100$ | Severe sea state. Complete suspension of nearshore and fishing operations. |
        """)
