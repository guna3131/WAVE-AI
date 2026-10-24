import streamlit as st
from frontend.components.header_banner import render_header_banner
from frontend.components.metric_cards import render_current_conditions_grid
from frontend.components.risk_card import render_hero_wave_activity_card
from frontend.components.explanation import render_feature_explanations
from frontend.components.wave_chart import create_wave_height_chart
from frontend.services.api import get_latest_conditions, get_historical_data
from frontend.services.prediction_service import predict_wave_activity
from frontend.config.config import STATION_KEY_TO_NAME
from frontend.utils.formatting import render_html

def render_dashboard_page():
    station_key = st.session_state.get("selected_station", "chennai")
    station_name = STATION_KEY_TO_NAME.get(station_key, "Chennai Coast")
    last_updated = st.session_state.get("last_updated", "2:29 PM")
    
    # 1. Header Banner
    render_header_banner(
        icon="🌊",
        title="WAVE AI",
        subtitle="AI-Based Coastal Wave Activity & Risk Prediction",
        station_name=station_name,
        last_updated=last_updated,
        refresh_button_label="Refresh Data",
        station_key=station_key
    )
    
    # Fetch real-time data
    conditions = get_latest_conditions(station_key)
    risk_info = predict_wave_activity(conditions)
    
    # 2. Current Conditions (6 Cards)
    render_current_conditions_grid(conditions)
    
    # 3. Hero Current Wave Activity Card
    render_hero_wave_activity_card(risk_info)
    
    # 4. Secondary Analytical Row (XAI Factors & 24h Trend Preview)
    col_chart, col_xai = st.columns([1.6, 1])
    
    with col_chart:
        render_html("""
        <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff; text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            <span>📈</span> 24-HOUR WAVE HEIGHT TREND
        </div>
        """)
        history_24h = get_historical_data(station_key, "Last 24 hours")
        fig = create_wave_height_chart(history_24h)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
    with col_xai:
        render_feature_explanations(conditions, risk_info)
