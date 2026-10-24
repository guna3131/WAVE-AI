import streamlit as st
import numpy as np
from frontend.components.header_banner import render_header_banner
from frontend.components.wave_chart import create_wave_height_chart, create_wave_period_chart
from frontend.services.api import get_historical_data
from frontend.config.config import STATION_KEY_TO_NAME
from frontend.utils.formatting import render_html

def render_wave_analysis_page():
    station_key = st.session_state.get("selected_station", "chennai")
    station_name = STATION_KEY_TO_NAME.get(station_key, "Chennai Coast")
    last_updated = st.session_state.get("last_updated", "2:29 PM")
    
    # 1. Header Banner
    render_header_banner(
        icon="📈",
        title="Wave Analysis",
        subtitle="Historical Metocean Behavior & Dynamic Ocean Trends",
        station_name=station_name,
        last_updated=last_updated,
        refresh_button_label="Refresh Analysis Data",
        station_key=station_key
    )
    
    # 2. Time Range Selector
    render_html('<div style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-bottom: 8px;">Select Time Range:</div>')
    
    time_options = ["Last 24 hours", "Last 3 days", "Last 7 days", "Last 30 days"]
    saved_tf = st.session_state.get("selected_timeframe", "Last 24 hours")
    selected_tf = st.radio(
        "Time Range Selector",
        time_options,
        index=time_options.index(saved_tf) if saved_tf in time_options else 0,
        horizontal=True,
        label_visibility="collapsed",
        key="time_range_radio"
    )
    st.session_state["selected_timeframe"] = selected_tf
    
    # Fetch historical data
    history = get_historical_data(station_key, selected_tf)
    
    # Calculate Summary Stats
    heights = [d["wave_height"] for d in history]
    winds = [d["wind_speed"] for d in history]
    pressures = [d["pressure"] for d in history]
    
    max_h = max(heights) if heights else 2.95
    mean_h = np.mean(heights) if heights else 2.39
    peak_w = max(winds) if winds else 22.5
    avg_p = np.mean(pressures) if pressures else 1008.0
    
    # 3. Four Summary Stats Indicators Row (Matching Reference Image 4)
    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        render_html(f"""
        <div style="padding: 10px 0;">
            <div style="font-size: 0.84rem; font-weight: 600; color: #cbd5e1; margin-bottom: 6px; display: flex; align-items: center; gap: 4px;">
                Max Wave Height <span style="font-size: 0.75rem; color: #64748b;">❔</span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff;">{max_h:.2f} m</div>
        </div>
        """)
        
    with c2:
        render_html(f"""
        <div style="padding: 10px 0;">
            <div style="font-size: 0.84rem; font-weight: 600; color: #cbd5e1; margin-bottom: 6px; display: flex; align-items: center; gap: 4px;">
                Mean Wave Height <span style="font-size: 0.75rem; color: #64748b;">❔</span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff;">{mean_h:.2f} m</div>
        </div>
        """)
        
    with c3:
        render_html(f"""
        <div style="padding: 10px 0;">
            <div style="font-size: 0.84rem; font-weight: 600; color: #cbd5e1; margin-bottom: 6px; display: flex; align-items: center; gap: 4px;">
                Peak Wind Speed <span style="font-size: 0.75rem; color: #64748b;">❔</span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff;">{peak_w:.1f} m/s</div>
        </div>
        """)
        
    with c4:
        render_html(f"""
        <div style="padding: 10px 0;">
            <div style="font-size: 0.84rem; font-weight: 600; color: #cbd5e1; margin-bottom: 6px; display: flex; align-items: center; gap: 4px;">
                Average Pressure <span style="font-size: 0.75rem; color: #64748b;">❔</span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff;">{avg_p:.1f} hPa</div>
        </div>
        """)
        
    render_html('<hr style="border: 0; border-top: 1px solid #162238; margin: 18px 0 24px 0;">')
    
    # 4. Synchronized Dual Plotly Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_h = create_wave_height_chart(history)
        st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar": False})
        
    with chart_col2:
        fig_p = create_wave_period_chart(history)
        st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})
