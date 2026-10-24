import streamlit as st
from typing import Dict, Any
from frontend.utils.formatting import render_html

def render_prediction_summary_cards(forecast_info: Dict[str, Any]):
    """
    Render 3 Prediction Summary Cards matching Reference Image 1.
    """
    peak_wave = forecast_info.get("peak_predicted_wave", 3.3)
    peak_time = forecast_info.get("peak_time", "2:29 AM")
    highest_risk = forecast_info.get("highest_risk_index", 65)
    highest_class = forecast_info.get("highest_risk_classification", "ROUGH")
    risk_window = forecast_info.get("elevated_risk_window", "3:29 PM - 2:29 AM")
    risk_sub = forecast_info.get("elevated_risk_subtext", "12 hours in Rough/Very Rough")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>PEAK PREDICTED WAVE</span>
                <span class="metric-icon">🌊</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold">{peak_wave:.1f}</span>
                <span class="metric-unit">m</span>
            </div>
            <div class="metric-subtext">Expected at {peak_time}</div>
        </div>
        """)
        
    with col2:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>HIGHEST RISK INDEX</span>
                <span class="metric-icon">⚠️</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold">{highest_risk}</span>
                <span class="metric-unit" style="color: #94a3b8; font-size: 0.95rem;">/ 100</span>
            </div>
            <div class="metric-subtext">Classification: <strong style="color: #f97316;">{highest_class}</strong></div>
        </div>
        """)
        
    with col3:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span>ELEVATED RISK WINDOW</span>
                <span class="metric-icon">⏱️</span>
            </div>
            <div class="metric-value-row">
                <span class="metric-value-bold" style="font-size: 1.45rem;">{risk_window}</span>
            </div>
            <div class="metric-subtext">{risk_sub}</div>
        </div>
        """)
        
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
