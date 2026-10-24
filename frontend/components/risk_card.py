import streamlit as st
from typing import Dict, Any
from frontend.utils.formatting import render_html

def render_hero_wave_activity_card(risk_info: Dict[str, Any]):
    """
    Render Hero Current Wave Activity Card matching Reference Image 3.
    """
    classification = risk_info.get("classification", "ROUGH")
    description = risk_info.get("description", "High wave energy and strong surf. Nearshore activities restricted.")
    
    orb_class_map = {
        "CALM": "glowing-orb-green",
        "MODERATE": "glowing-orb-yellow",
        "ROUGH": "glowing-orb-orange",
        "VERY ROUGH": "glowing-orb-red"
    }
    
    color_map = {
        "CALM": "#10b981",
        "MODERATE": "#f59e0b",
        "ROUGH": "#f97316",
        "VERY ROUGH": "#ef4444"
    }
    
    orb_class = orb_class_map.get(classification, "glowing-orb-orange")
    text_color = color_map.get(classification, "#f97316")
    
    render_html(f"""
    <div class="hero-activity-card" style="border-color: {text_color};">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div class="glowing-orb {orb_class}"></div>
            <div>
                <div style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; color: #94a3b8; text-transform: uppercase; margin-bottom: 2px;">
                    CURRENT WAVE ACTIVITY
                </div>
                <div style="font-size: 2.3rem; font-weight: 900; color: {text_color}; line-height: 1.1; margin-bottom: 4px;">
                    {classification}
                </div>
                <div style="font-size: 0.85rem; color: #cbd5e1;">
                    {description}
                </div>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">
                FORECAST WINDOW
            </div>
            <div class="forecast-window-badge">
                ⏱️ Next 6 Hours
            </div>
        </div>
    </div>
    """)
