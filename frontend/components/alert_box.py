import streamlit as st
from typing import Dict, Any
from frontend.utils.formatting import render_html

def render_coastal_alerts_view(alert_info: Dict[str, Any]):
    """
    Render Coastal Alerts & Operational Recommendations matching Reference Image 2.
    """
    render_html("""
    <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff; text-transform: uppercase; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
        <span>⚠️</span> CURRENT ALERT STATUS
    </div>
    """)
    
    station_name = alert_info.get("station_name", "Chennai Coast")
    title = alert_info.get("alert_title", "HIGH WAVE ACTIVITY — ROUGH ADVISORY")
    expected_hs = alert_info.get("expected_wave_height", 3.4)
    risk_score = alert_info.get("risk_score", 66)
    prob = alert_info.get("probability", "81%")
    horizon = alert_info.get("expected_horizon", "Within 6 hours")
    note = alert_info.get("advisory_note", "Noticeable wave surge. Small craft operators advised to exercise extreme caution near breaking reefs and bar entrances.")
    
    # Hero Alert Status Card
    render_html(f"""
    <div class="hero-alert-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div class="glowing-orb glowing-orb-orange"></div>
                <div>
                    <div style="font-size: 0.70rem; font-weight: 700; letter-spacing: 0.08em; color: #cbd5e1; text-transform: uppercase;">
                        CURRENT ALERT STATUS
                    </div>
                    <div style="font-size: 1.65rem; font-weight: 900; color: #ffffff; margin-top: 2px;">
                        {title}
                    </div>
                </div>
            </div>
            <div class="forecast-window-badge" style="background: rgba(0,0,0,0.4); border-color: rgba(249, 115, 22, 0.4);">
                Location: <strong>{station_name}</strong>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 18px;">
            <div class="alert-metric-col">
                <div class="alert-metric-label">EXPECTED WAVE HEIGHT</div>
                <div class="alert-metric-val">{expected_hs:.1f} m</div>
            </div>
            <div class="alert-metric-col">
                <div class="alert-metric-label">RISK SCORE</div>
                <div class="alert-metric-val-orange">{risk_score} <span style="font-size: 1rem; color: #94a3b8;">/ 100</span></div>
            </div>
            <div class="alert-metric-col">
                <div class="alert-metric-label">PROBABILITY</div>
                <div class="alert-metric-val">{prob}</div>
            </div>
            <div class="alert-metric-col">
                <div class="alert-metric-label">EXPECTED HORIZON</div>
                <div class="alert-metric-val" style="font-size: 1.25rem;">{horizon}</div>
            </div>
        </div>
        <div class="alert-note-box">
            <strong style="color: #fb923c;">Advisory Note:</strong> {note}
        </div>
    </div>
    """)
    
    st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)
    
    # Operational Maritime Recommendations (3 Cards)
    render_html("""
    <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff; text-transform: uppercase; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
        <span>⚓</span> OPERATIONAL MARITIME RECOMMENDATIONS
    </div>
    """)
    
    recs = alert_info.get("recommendations", {})
    r_craft = recs.get("small_craft", "Ensure VHF radio communications are active on Channel 16. If wave heights exceed 2.5m, suspend deep-sea artisanal fishing trips.")
    r_port = recs.get("port_ops", "Monitor harbor surge oscillations and mooring tensions. Pilotage services may require tug assistance during rough swell windows.")
    r_rec = recs.get("recreation", "Red flags indicate strong rip currents and crashing breaker waves. Swimming and beach shoreline water-sports restricted.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_html(f"""
        <div class="recommendation-card">
            <div class="rec-header">
                <span>SMALL CRAFT & FISHERMEN</span>
                <span style="font-size: 1.2rem;">🚤</span>
            </div>
            <div class="rec-text">{r_craft}</div>
        </div>
        """)
        
    with col2:
        render_html(f"""
        <div class="recommendation-card">
            <div class="rec-header">
                <span>PORT & HARBOR OPS</span>
                <span style="font-size: 1.2rem;">🚢</span>
            </div>
            <div class="rec-text">{r_port}</div>
        </div>
        """)
        
    with col3:
        render_html(f"""
        <div class="recommendation-card">
            <div class="rec-header">
                <span>COASTAL RECREATION</span>
                <span style="font-size: 1.2rem;">🏖️</span>
            </div>
            <div class="rec-text">{r_rec}</div>
        </div>
        """)
