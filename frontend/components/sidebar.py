import streamlit as st
from frontend.config.config import STATIONS, STATION_MAP, STATION_KEY_TO_NAME
from frontend.services.api import trigger_refresh
from frontend.utils.constants import NAVIGATION_ITEMS
from frontend.utils.formatting import render_html

def render_sidebar():
    """
    Render sidebar exactly matching the reference images.
    """
    with st.sidebar:
        # 1. Branding Header
        render_html("""
        <div style="padding-top: 10px; margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                <span style="font-size: 2rem;">🌊</span>
                <span style="font-size: 1.55rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">WAVE AI</span>
            </div>
            <div style="font-size: 0.80rem; color: #38bdf8; font-weight: 500; line-height: 1.3;">
                AI-Based Coastal Wave Activity & Risk Prediction
            </div>
        </div>
        """)
        
        # 2. Location Picker
        render_html('<div class="sidebar-section-header">📍 COASTAL LOCATION</div>')
        
        station_names = [s["name"] for s in STATIONS]
        current_station_key = st.session_state.get("selected_station", "chennai")
        current_name = STATION_KEY_TO_NAME.get(current_station_key, "Chennai Coast")
        
        current_index = station_names.index(current_name) if current_name in station_names else 0
        selected_name = st.selectbox(
            "Select Coastal Location",
            station_names,
            index=current_index,
            label_visibility="collapsed",
            key="location_selector"
        )
        
        selected_key = STATION_MAP[selected_name]
        if selected_key != current_station_key:
            st.session_state["selected_station"] = selected_key
            st.rerun()
            
        # 3. Data Status Card
        last_updated = st.session_state.get("last_updated", "2:29 PM")
        render_html(f"""
        <div class="sidebar-section-header">DATA STATUS</div>
        <div class="sidebar-status-card">
            <div class="status-badge-green">
                <span style="font-size: 0.75rem;">🟢</span> Data Available
            </div>
            <div class="status-time-sub">
                Last Updated: <strong style="color: #f1f5f9;">{last_updated}</strong>
            </div>
        </div>
        """)
        
        # 4. Cyan Full-Width Refresh Button
        if st.button("🔄 Refresh Data", use_container_width=True, type="primary", key="sidebar_refresh_btn"):
            ts = trigger_refresh(selected_key)
            st.toast(f"✅ Live data refreshed for {selected_name} at {ts}!", icon="🌊")
            st.rerun()
            
        # 5. Navigation Items
        render_html('<div class="sidebar-section-header" style="margin-top: 1.8rem;">NAVIGATION</div>')
        
        current_page = st.session_state.get("current_page", "dashboard")
        for item in NAVIGATION_ITEMS:
            is_active = (current_page == item["key"])
            btn_style = "primary" if is_active else "secondary"
            btn_label = f"{item['icon']}  {item['label']}"
            
            if st.button(
                btn_label,
                key=f"nav_{item['key']}",
                use_container_width=True,
                type=btn_style
            ):
                if current_page != item["key"]:
                    st.session_state["current_page"] = item["key"]
                    st.rerun()
