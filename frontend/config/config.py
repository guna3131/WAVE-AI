"""
WAVE AI - Application Configuration & Station Registry.
"""

APP_TITLE = "WAVE AI"
APP_SUBTITLE = "AI-Based Coastal Wave Activity & Risk Prediction"
APP_ICON = "🌊"

# Stations available in the sidebar dropdown
STATIONS = [
    {"key": "chennai", "name": "Chennai Coast", "basin": "Bay of Bengal", "buoy_id": "BD08"},
    {"key": "pondicherry", "name": "Pondicherry Coast", "basin": "Bay of Bengal", "buoy_id": "BD09"},
    {"key": "nagapattinam", "name": "Nagapattinam Coast", "basin": "Bay of Bengal", "buoy_id": "BD10"},
    {"key": "kanyakumari", "name": "Kanyakumari Coast", "basin": "Tri-Sea Confluence", "buoy_id": "IO01"},
    {"key": "visakhapatnam", "name": "Visakhapatnam Coast", "basin": "Deep-Water Bay", "buoy_id": "BD06"},
    {"key": "mumbai", "name": "Mumbai Coast", "basin": "Arabian Sea", "buoy_id": "AD02"},
    {"key": "buoy_41002", "name": "NOAA Buoy 41002 (South Hatteras)", "basin": "Atlantic Ocean", "buoy_id": "41002"},
    {"key": "buoy_46042", "name": "NOAA Buoy 46042 (Monterey Bay)", "basin": "Pacific Ocean", "buoy_id": "46042"}
]

STATION_MAP = {s["name"]: s["key"] for s in STATIONS}
STATION_KEY_TO_NAME = {s["key"]: s["name"] for s in STATIONS}

# Classification thresholds for Hs in meters
CALM_THRESHOLD = 1.5
MODERATE_THRESHOLD = 2.5
ROUGH_THRESHOLD = 3.5
