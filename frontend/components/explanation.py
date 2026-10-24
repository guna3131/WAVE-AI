import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any
from frontend.utils.formatting import render_html

def render_feature_explanations(conditions: Dict[str, Any], risk_info: Dict[str, Any]):
    """
    Render Explainable AI (XAI) feature contribution breakdown.
    """
    render_html("""
    <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff; text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
        <span>💡</span> EXPLAINABLE AI — RISK CONTRIBUTING FACTORS
    </div>
    """)
    
    hs = float(conditions.get("wave_height", 2.7))
    wspd = float(conditions.get("wind_speed", 21.2))
    tp = float(conditions.get("wave_period", 9.4))
    pressure = float(conditions.get("pressure", 1008.0))
    
    # Normalized feature contributions (relative weights out of 100)
    c_hs = round(min(50.0, (hs / 3.5) * 50.0), 1)
    c_wind = round(min(25.0, (wspd / 25.0) * 25.0), 1)
    c_steepness = round(min(15.0, (hs / (1.56 * (tp**2))) * 250), 1)
    c_pressure = round(min(10.0, max(0.0, 1013.0 - pressure) * 2.0), 1)
    
    factors = ["Wave Height (Hs)", "Wind Drag Stress", "Wave Steepness (H/L)", "Barometric Dip"]
    scores = [c_hs, c_wind, c_steepness, c_pressure]
    
    fig = go.Figure(go.Bar(
        x=scores,
        y=factors,
        orientation="h",
        marker=dict(
            color=["#00d2ff", "#38bdf8", "#818cf8", "#f43f5e"],
            line=dict(width=0)
        ),
        text=[f"{s}%" for s in scores],
        textposition="outside",
        textfont=dict(color="#cbd5e1", size=11)
    ))
    
    fig.update_layout(
        paper_bgcolor="#0f1c30",
        plot_bgcolor="#0f1c30",
        height=180,
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 60]),
        yaxis=dict(tickfont=dict(color="#cbd5e1", size=11), autorange="reversed"),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
