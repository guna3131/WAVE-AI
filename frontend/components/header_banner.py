import streamlit as st
from frontend.services.api import trigger_refresh
from frontend.utils.formatting import render_html

def render_header_banner(
    icon: str,
    title: str,
    subtitle: str,
    station_name: str,
    last_updated: str,
    refresh_button_label: str = "Refresh Data",
    station_key: str = "chennai"
):
    """
    Render top header banner card matching the reference images.
    """
    col_content, col_action = st.columns([5, 1.3])
    
    with col_content:
        render_html(f"""
        <div class="header-banner-card" style="margin-bottom: 0;">
            <div class="header-title">
                <span>{icon}</span> {title}
            </div>
            <div class="header-subtitle">{subtitle}</div>
            <div class="header-meta-row">
                <span style="font-weight: 600; color: #ffffff;">📍 {station_name}</span>
                <span class="pill-badge">
                    <span style="font-size: 0.65rem;">🟢</span> Live Data Available
                </span>
                <span style="color: #94a3b8;">Last Updated: <strong style="color: #f1f5f9;">{last_updated}</strong></span>
            </div>
        </div>
        """)
        
    with col_action:
        # Align refresh button inside same visual horizontal band
        st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
        if st.button(f"🔄 {refresh_button_label}", use_container_width=True, key=f"banner_ref_{title.replace(' ', '_')}"):
            ts = trigger_refresh(station_key)
            st.toast(f"✅ Live data refreshed for {station_name} at {ts}!", icon="🌊")
            st.rerun()
            
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
