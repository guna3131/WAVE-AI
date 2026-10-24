import streamlit as st
from frontend.components.header_banner import render_header_banner
from frontend.config.config import STATION_KEY_TO_NAME, STATIONS
from frontend.utils.formatting import render_html

def render_about_page():
    station_key = st.session_state.get("selected_station", "chennai")
    station_name = STATION_KEY_TO_NAME.get(station_key, "Chennai Coast")
    last_updated = st.session_state.get("last_updated", "2:29 PM")
    
    # 1. Header Banner
    render_header_banner(
        icon="ℹ️",
        title="About WAVE AI",
        subtitle="AI-Powered Coastal Wave Activity & Marine Risk Prediction System",
        station_name=station_name,
        last_updated=last_updated,
        refresh_button_label="Refresh Data",
        station_key=station_key
    )
    
    # 2. Creator & Lead Developer Profile Card
    render_html("""
    <div class="creator-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <div class="creator-avatar">👨‍💻</div>
                <div>
                    <div style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; color: #38bdf8; text-transform: uppercase;">
                        PROJECT CREATOR & LEAD ARCHITECT
                    </div>
                    <div style="font-size: 1.85rem; font-weight: 900; color: #ffffff; margin-top: 2px;">
                        Guna Nagaraj
                    </div>
                    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 2px;">
                        AI/ML Engineer & Coastal Metocean Systems Architect
                    </div>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; color: #94a3b8; text-transform: uppercase;">
                    SYSTEM VERSION
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #00d2ff; margin-top: 2px;">
                    v2.4.0 Production Build
                </div>
                <div style="font-size: 0.78rem; color: #10b981; font-weight: 600; margin-top: 2px;">
                    🟢 Live Telemetry Engine Active
                </div>
            </div>
        </div>
        
        <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 0.88rem; color: #cbd5e1; line-height: 1.6;">
            <strong>WAVE AI</strong> was conceived and created by <strong>Guna Nagaraj</strong> to address the urgent need for accessible, high-precision coastal wave hazard intelligence. By marrying physical oceanographic modeling (Pierson-Moskowitz, deep-water dispersion, and wind drag stresses) with modern machine learning risk scoring and real-time NOAA ERDDAP buoy telemetry, WAVE AI empowers artisanal fishermen, commercial port operators, and coastal safety authorities with immediate, actionable forecasts.
        </div>
        
        <div style="margin-top: 14px;">
            <span class="tech-badge">Python 3.14</span>
            <span class="tech-badge">Streamlit 1.62</span>
            <span class="tech-badge">Plotly 6.9</span>
            <span class="tech-badge">NOAA ERDDAP REST API</span>
            <span class="tech-badge">Open-Meteo High-Res Marine</span>
            <span class="tech-badge">Hydrodynamic Physics</span>
            <span class="tech-badge">Explainable AI (XAI)</span>
        </div>
    </div>
    """)
    
    # 3. System Architecture & Flow (Modern Grid Cards instead of raw ASCII)
    render_html("""
    <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff; text-transform: uppercase; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
        <span>🌊</span> SYSTEM ARCHITECTURE & CORE PIPELINE
    </div>
    """)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        render_html("""
        <div class="about-feature-box">
            <div style="font-size: 0.75rem; font-weight: 700; color: #00d2ff; text-transform: uppercase; margin-bottom: 6px;">
                01. LIVE INGESTION
            </div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
                Multi-Source Metocean Ingestion
            </div>
            <div style="font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">
                Streams sub-hourly wave height, dominant wave period, swell, surface wind, and barometric pressure from NOAA ERDDAP buoys and live high-resolution coastal feeds.
            </div>
        </div>
        """)
    with c2:
        render_html("""
        <div class="about-feature-box">
            <div style="font-size: 0.75rem; font-weight: 700; color: #a855f7; text-transform: uppercase; margin-bottom: 6px;">
                02. HYDRODYNAMICS
            </div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
                Feature Engineering Pipeline
            </div>
            <div style="font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">
                Applies gravity wave dispersion theory to compute wavelength (&lambda; &approx; 1.56 &middot; Tp&sup2;), wave steepness (Hs / &lambda;), and air-sea momentum drag stresses.
            </div>
        </div>
        """)
    with c3:
        render_html("""
        <div class="about-feature-box">
            <div style="font-size: 0.75rem; font-weight: 700; color: #10b981; text-transform: uppercase; margin-bottom: 6px;">
                03. PREDICTIVE AI
            </div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
                Risk Classifier & 12h Forecast
            </div>
            <div style="font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">
                Evaluates a 0–100 composite marine hazard score, predicts 12-hour forward wave trajectories with 90% confidence bands, and generates Explainable AI (XAI) feature impacts.
            </div>
        </div>
        """)
        
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
    
    # 4. Oceanographic Mathematical Formulations
    render_html("""
    <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff; text-transform: uppercase; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
        <span>📐</span> HYDRODYNAMIC & PHYSICAL FORMULAS
    </div>
    """)
    
    f1, f2 = st.columns(2)
    with f1:
        st.markdown(r"""
        **1. Deep-Water Wavelength & Gravity Dispersion ($\lambda$)**:
        $$\lambda \approx \frac{g}{2\pi} T_p^2 \approx 1.56 \cdot T_p^2$$
        *Calculates horizontal wave spatial extent from the peak period ($T_p$) in seconds.*
        
        **2. Wave Steepness Breaking Criterion ($S$)**:
        $$S = \frac{H_s}{\lambda}$$
        *When $S > 0.04 - 0.05$, waves exceed stability limits and enter dangerous breaking surf.*
        """)
    with f2:
        st.markdown(r"""
        **3. Sea Surface Wind Drag Stress ($\tau$)**:
        $$\tau = \rho_{air} \cdot C_d \cdot V_{wind}^2$$
        *Quantifies kinetic energy transfer from sustained surface wind velocities into wave surge.*
        
        **4. Composite Marine Risk Index ($0 - 100$)**:
        $$\text{Risk Score} = 60 \cdot \text{Norm}(H_s) + 25 \cdot \text{Norm}(V_{wind}) + 15 \cdot \text{Norm}(\Delta P)$$
        *Calibrated multi-factor safety assessment for coastal and harbor operations.*
        """)
        
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
    
    # 5. Monitored Stations Registry Table
    render_html("""
    <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff; text-transform: uppercase; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
        <span>📍</span> MONITORED STATIONS & BUOY REGISTRY
    </div>
    """)
    
    station_rows = []
    for s in STATIONS:
        station_rows.append({
            "Station Name": s["name"],
            "Ocean Basin": s["basin"],
            "Buoy Identifier": s["buoy_id"],
            "Telemetry Source": "NOAA CoastWatch ERDDAP" if "41002" in s["buoy_id"] or "46042" in s["buoy_id"] else "Real-Time Coastal Marine Feed",
            "Status": "🟢 Active Live"
        })
    import pandas as pd
    st.dataframe(pd.DataFrame(station_rows), use_container_width=True, hide_index=True)
    
    st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)
    
    # 6. Safety Notice
    render_html("""
    <div style="background: rgba(249, 115, 22, 0.08); border: 1px solid rgba(249, 115, 22, 0.3); border-radius: 10px; padding: 16px 20px; font-size: 0.85rem; color: #fed7aa; line-height: 1.5;">
        <strong style="color: #f97316;">⚠️ Prototype Safety Notice:</strong> WAVE AI is a machine-learning and metocean research platform created by Guna Nagaraj. Predictions and risk categories should not be treated as official government disaster warnings. For emergency evacuations and official maritime notices, always consult national agencies (INCOIS, IMD, NOAA).
    </div>
    """)
