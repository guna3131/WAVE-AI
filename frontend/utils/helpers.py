import streamlit as st
import datetime

def init_session_state():
    """
    Ensure all required session state variables are initialized safely.
    """
    if "selected_station" not in st.session_state:
        st.session_state["selected_station"] = "chennai"
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "dashboard"
    if "last_updated" not in st.session_state:
        st.session_state["last_updated"] = datetime.datetime.now().strftime("%I:%M %p")
    if "data_status" not in st.session_state:
        st.session_state["data_status"] = "Data Available"
    if "refresh_counter" not in st.session_state:
        st.session_state["refresh_counter"] = 0
    if "selected_timeframe" not in st.session_state:
        st.session_state["selected_timeframe"] = "Last 24 hours"

def update_refresh_timestamp():
    """
    Update the last refreshed timestamp across the session safely.
    """
    now_str = datetime.datetime.now().strftime("%I:%M %p")
    try:
        if "refresh_counter" not in st.session_state:
            st.session_state["refresh_counter"] = 0
        st.session_state["refresh_counter"] += 1
        st.session_state["last_updated"] = now_str
    except Exception:
        pass
    return now_str
