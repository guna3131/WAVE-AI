import streamlit as st
import pandas as pd
from frontend.components.header_banner import render_header_banner
from frontend.components.prediction_card import render_prediction_summary_cards
from frontend.components.wave_chart import create_12h_trajectory_chart
from frontend.services.api import get_latest_conditions
from frontend.services.prediction_service import get_12h_forecast
from frontend.config.config import STATION_KEY_TO_NAME
from frontend.utils.formatting import render_html

def render_predictions_page():
    station_key = st.session_state.get("selected_station", "chennai")
    station_name = STATION_KEY_TO_NAME.get(station_key, "Chennai Coast")
    last_updated = st.session_state.get("last_updated", "2:29 PM")
    
    # 1. Header Banner
    render_header_banner(
        icon="🔮",
        title="Wave Activity Predictions",
        subtitle="Machine Learning Powered Coastal Wave Height & Risk Outlook",
        station_name=station_name,
        last_updated=last_updated,
        refresh_button_label="Refresh Prediction",
        station_key=station_key
    )
    
    # Fetch current observations & generate 12h forecast
    conditions = get_latest_conditions(station_key)
    forecast_info = get_12h_forecast(conditions)
    
    # 2. Prediction Summary Cards (3 Cards)
    render_prediction_summary_cards(forecast_info)
    
    # 3. 12-Hour Forward Wave Height Trajectory Section
    render_html("""
    <div style="font-size: 0.95rem; font-weight: 700; color: #ffffff; margin-bottom: 12px;">
        12-Hour Forward Wave Height Trajectory
    </div>
    """)
    
    fig = create_12h_trajectory_chart(forecast_info["points"])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    # 4. Hourly Forecast Schedule Table
    with st.expander("📋 View Hourly Wave Forecast Data Table", expanded=False):
        table_rows = []
        for p in forecast_info["points"]:
            table_rows.append({
                "Forecast Offset": p["hour_offset"],
                "Expected Time": p["time"],
                "Predicted Height": f"{p['predicted_height']:.2f} m",
                "Confidence Interval (90%)": f"{p['lower_bound']:.2f} m - {p['upper_bound']:.2f} m",
                "Risk Classification": p["classification"]
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
