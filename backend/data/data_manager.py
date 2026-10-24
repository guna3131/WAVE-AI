import time
import datetime
from typing import Dict, Any, List, Optional
from backend.data.erddap_client import fetch_buoy_latest, fetch_buoy_history
from backend.data.marine_api_client import fetch_coastal_conditions, fetch_coastal_history
from backend.data.mock_buoy_feed import generate_current_conditions, generate_historical_series

STATION_COORDINATES = {
    "chennai": {"name": "Chennai Coast", "lat": 13.0827, "lon": 80.2707, "buoy_id": "BD08", "type": "coastal"},
    "pondicherry": {"name": "Pondicherry Coast", "lat": 11.9416, "lon": 79.8083, "buoy_id": "BD09", "type": "coastal"},
    "nagapattinam": {"name": "Nagapattinam Coast", "lat": 10.7672, "lon": 79.8424, "buoy_id": "BD10", "type": "coastal"},
    "kanyakumari": {"name": "Kanyakumari Coast", "lat": 8.0883, "lon": 77.5385, "buoy_id": "IO01", "type": "coastal"},
    "visakhapatnam": {"name": "Visakhapatnam Coast", "lat": 17.6868, "lon": 83.2185, "buoy_id": "BD06", "type": "coastal"},
    "mumbai": {"name": "Mumbai Coast", "lat": 18.9220, "lon": 72.8347, "buoy_id": "AD02", "type": "coastal"},
    "buoy_41002": {"name": "NOAA Buoy 41002 (South Hatteras)", "lat": 31.758, "lon": -74.836, "buoy_id": "41002", "type": "erddap"},
    "buoy_46042": {"name": "NOAA Buoy 46042 (Monterey Bay)", "lat": 36.785, "lon": -122.404, "buoy_id": "46042", "type": "erddap"},
}

# Cache structure: {station_key: {"timestamp": float, "data": dict}}
_CACHE_CURRENT: Dict[str, Dict[str, Any]] = {}
_CACHE_HISTORY: Dict[str, Dict[str, Any]] = {}
CACHE_TTL_SECONDS = 300  # 5 minutes default TTL

def get_current_conditions(station_key: str = "chennai", force_refresh: bool = False) -> Dict[str, Any]:
    """
    Retrieve real-time conditions for a station with cache control and failover.
    """
    station_key = station_key.lower()
    now_ts = time.time()
    
    # Check cache if not forcing refresh
    if not force_refresh and station_key in _CACHE_CURRENT:
        cached = _CACHE_CURRENT[station_key]
        if now_ts - cached["ts"] < CACHE_TTL_SECONDS:
            return cached["data"]
            
    info = STATION_COORDINATES.get(station_key, STATION_COORDINATES["chennai"])
    station_type = info["type"]
    result: Optional[Dict[str, Any]] = None
    
    # 1. Try real-time live ingestion
    try:
        if station_type == "erddap":
            result = fetch_buoy_latest(info["buoy_id"])
        elif station_type == "coastal":
            result = fetch_coastal_conditions(info["lat"], info["lon"])
    except Exception:
        result = None
        
    # 2. If live API returned None, fallback gracefully
    if not result:
        result = generate_current_conditions(station_key)
        
    # Attach station metadata
    result["station_key"] = station_key
    result["station_name"] = info["name"]
    result["station_id"] = info["buoy_id"]
    result["latitude"] = info["lat"]
    result["longitude"] = info["lon"]
    result["last_updated_time"] = datetime.datetime.now().strftime("%I:%M %p")
    result["last_updated_iso"] = datetime.datetime.now().isoformat()
    
    # Store in cache
    _CACHE_CURRENT[station_key] = {"ts": now_ts, "data": result}
    return result

def get_station_history(station_key: str = "chennai", timeframe: str = "24h", force_refresh: bool = False) -> List[Dict[str, Any]]:
    """
    Retrieve historical time-series observations for a station.
    Timeframe options: '24h', '3d', '7d', '30d'
    """
    station_key = station_key.lower()
    now_ts = time.time()
    cache_key = f"{station_key}_{timeframe}"
    
    if not force_refresh and cache_key in _CACHE_HISTORY:
        cached = _CACHE_HISTORY[cache_key]
        if now_ts - cached["ts"] < CACHE_TTL_SECONDS:
            return cached["data"]
            
    info = STATION_COORDINATES.get(station_key, STATION_COORDINATES["chennai"])
    
    hours_map = {
        "24h": 24,
        "3d": 72,
        "7d": 168,
        "30d": 720
    }
    days_map = {
        "24h": 1,
        "3d": 3,
        "7d": 7,
        "30d": 30
    }
    hours = hours_map.get(timeframe, 24)
    days = days_map.get(timeframe, 1)
    
    history: Optional[List[Dict[str, Any]]] = None
    try:
        if info["type"] == "erddap":
            history = fetch_buoy_history(info["buoy_id"], hours=min(hours, 72))
        elif info["type"] == "coastal":
            history = fetch_coastal_history(info["lat"], info["lon"], days=days)
    except Exception:
        history = None
        
    if not history or len(history) < 5:
        history = generate_historical_series(station_key, hours=hours)
        
    _CACHE_HISTORY[cache_key] = {"ts": now_ts, "data": history}
    return history
