import os
import streamlit as st

# Configure wide layout, ocean icon, and title
st.set_page_config(
    page_title="WAVE AI - Coastal Wave Activity & Risk Prediction",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Invert / inject custom ocean dark styling
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from frontend.utils.helpers import init_session_state
from frontend.components.sidebar import render_sidebar
from frontend.views.dashboard import render_dashboard_page
from frontend.views.wave_analysis import render_wave_analysis_page
from frontend.views.predictions import render_predictions_page
from frontend.views.alerts import render_alerts_page
from frontend.views.about import render_about_page

# 1. Initialize persistent state
init_session_state()

# 2. Render sidebar (Branding, Location Selector, Data Status, Refresh Button, Navigation)
render_sidebar()

# 3. Page Router
current_page = st.session_state.get("current_page", "dashboard")

if current_page == "dashboard":
    render_dashboard_page()
elif current_page == "wave_analysis":
    render_wave_analysis_page()
elif current_page == "predictions":
    render_predictions_page()
elif current_page == "alerts":
    render_alerts_page()
elif current_page == "about":
    render_about_page()
else:
    render_dashboard_page()
