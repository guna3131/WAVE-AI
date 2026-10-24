import streamlit as st
from typing import Dict, Any, List
from backend.data.data_manager import get_current_conditions, get_station_history
from backend.models.model_loader import evaluate_risk
from backend.database.db import log_telemetry
from frontend.utils.helpers import update_refresh_timestamp

def get_latest_conditions(station_key: str = "chennai", force_refresh: bool = False) -> Dict[str, Any]:
    """
    Fetch latest metocean conditions from the data broker.
    """
    data = get_current_conditions(station_key, force_refresh=force_refresh)
    if force_refresh:
        update_refresh_timestamp()
        risk_info = evaluate_risk(data)
        log_telemetry(data, risk_info)
    return data

def get_historical_data(station_key: str = "chennai", timeframe_label: str = "Last 24 hours", force_refresh: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch historical metocean data series for a given timeframe label.
    """
    mapping = {
        "Last 24 hours": "24h",
        "Last 3 days": "3d",
        "Last 7 days": "7d",
        "Last 30 days": "30d"
    }
    tf = mapping.get(timeframe_label, "24h")
    return get_station_history(station_key, timeframe=tf, force_refresh=force_refresh)

def trigger_refresh(station_key: str) -> str:
    """
    Execute on-demand live data refresh, busting all local caches and updating timestamps.
    """
    data = get_current_conditions(station_key, force_refresh=True)
    ts = update_refresh_timestamp()
    risk_info = evaluate_risk(data)
    log_telemetry(data, risk_info)
    return ts
