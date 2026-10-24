import streamlit as st
from typing import Dict, Any
from frontend.utils.formatting import degrees_to_compass, render_html

def render_current_conditions_grid(conditions: Dict[str, Any]):
    """
    Render the 6 metocean metric cards matching Reference Image 3.
    """
    render_html("""
    <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff; text-transform: uppercase; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
        <span>🌊</span> CURRENT CONDITIONS
    </div>
    """)
    
    hs = float(conditions.get("wave_height", 2.7))
    tp = float(conditions.get("wave_period", 9.4))
    wspd = float(conditions.get("wind_speed", 21.2))
    wdir = float(conditions.get("wind_direction", 121.0))
    compass_dir = degrees_to_compass(wdir)
    temp = float(conditions.get("temperature", 30.8))
    pressure = int(round(float(conditions.get("pressure", 1008.0))))
    
    # Row 1: 4 cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>WAVE HEIGHT</span>
                <span class="metric-icon">🌊</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold">{hs:.1f}</span>
                <span class="metric-unit">m</span>
            </div>
            <div class="metric-subtext">Significant wave height (Hs)</div>
        </div>
        """)
        
    with col2:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>WAVE PERIOD</span>
                <span class="metric-icon">⏱️</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold">{tp:.1f}</span>
                <span class="metric-unit">s</span>
            </div>
            <div class="metric-subtext">Dominant peak period (Tp)</div>
        </div>
        """)
        
    with col3:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>WIND SPEED</span>
                <span class="metric-icon">💨</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold">{wspd:.1f}</span>
                <span class="metric-unit">m/s</span>
            </div>
            <div class="metric-subtext">Sustained surface wind</div>
        </div>
        """)
        
    with col4:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>WIND DIRECTION</span>
                <span class="metric-icon">🧭</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold">{int(wdir)}</span>
                <span class="metric-unit">°</span>
            </div>
            <div class="metric-subtext">{compass_dir}</div>
        </div>
        """)
        
    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)
    
    # Row 2: 2 cards
    col5, col6 = st.columns(2)
    
    with col5:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>SEA SURFACE / AIR TEMP</span>
                <span class="metric-icon">🌡️</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold">{temp:.1f}</span>
                <span class="metric-unit">°C</span>
            </div>
            <div class="metric-subtext">Ambient coastal temperature</div>
        </div>
        """)
        
    with col6:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>ATMOSPHERIC PRESSURE</span>
                <span class="metric-icon">🧭</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold">{pressure}</span>
                <span class="metric-unit">hPa</span>
            </div>
            <div class="metric-subtext">Barometric sea-level pressure</div>
        </div>
        """)
