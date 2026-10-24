import math
import random
import datetime
from typing import Dict, Any, List

# Station profile templates
STATION_PROFILES = {
    "chennai": {
        "name": "Chennai Coast",
        "buoy_id": "BD08",
        "base_wave": 2.7,
        "base_period": 9.4,
        "base_wind": 21.2,
        "base_dir": 121.0,
        "base_temp": 30.8,
        "base_pressure": 1008.0,
        "roughness": "ROUGH"
    },
    "pondicherry": {
        "name": "Pondicherry Coast",
        "buoy_id": "BD09",
        "base_wave": 1.9,
        "base_period": 8.6,
        "base_wind": 15.4,
        "base_dir": 115.0,
        "base_temp": 29.8,
        "base_pressure": 1010.0,
        "roughness": "MODERATE"
    },
    "nagapattinam": {
        "name": "Nagapattinam Coast",
        "buoy_id": "BD10",
        "base_wave": 2.4,
        "base_period": 9.1,
        "base_wind": 18.6,
        "base_dir": 130.0,
        "base_temp": 30.2,
        "base_pressure": 1009.0,
        "roughness": "MODERATE"
    },
    "kanyakumari": {
        "name": "Kanyakumari Coast",
        "buoy_id": "IO01",
        "base_wave": 3.6,
        "base_period": 11.2,
        "base_wind": 26.5,
        "base_dir": 195.0,
        "base_temp": 28.5,
        "base_pressure": 1006.0,
        "roughness": "VERY ROUGH"
    },
    "visakhapatnam": {
        "name": "Visakhapatnam Coast",
        "buoy_id": "BD06",
        "base_wave": 2.1,
        "base_period": 8.8,
        "base_wind": 16.8,
        "base_dir": 110.0,
        "base_temp": 30.0,
        "base_pressure": 1009.5,
        "roughness": "MODERATE"
    },
    "mumbai": {
        "name": "Mumbai Coast",
        "buoy_id": "AD02",
        "base_wave": 1.3,
        "base_period": 7.5,
        "base_wind": 11.2,
        "base_dir": 240.0,
        "base_temp": 29.2,
        "base_pressure": 1012.0,
        "roughness": "CALM"
    },
    "buoy_41002": {
        "name": "NOAA Buoy 41002 (South Hatteras)",
        "buoy_id": "41002",
        "base_wave": 2.6,
        "base_period": 9.0,
        "base_wind": 19.5,
        "base_dir": 210.0,
        "base_temp": 27.8,
        "base_pressure": 1011.5,
        "roughness": "ROUGH"
    },
    "buoy_46042": {
        "name": "NOAA Buoy 46042 (Monterey Bay)",
        "buoy_id": "46042",
        "base_wave": 1.8,
        "base_period": 12.0,
        "base_wind": 13.0,
        "base_dir": 290.0,
        "base_temp": 16.5,
        "base_pressure": 1015.0,
        "roughness": "MODERATE"
    }
}

def generate_current_conditions(station_key: str = "chennai") -> Dict[str, Any]:
    """
    Generate realistic hydrodynamic current metocean conditions for offline or fallback mode.
    """
    profile = STATION_PROFILES.get(station_key.lower(), STATION_PROFILES["chennai"])
    now = datetime.datetime.now()
    
    # Small deterministic diurnal drift based on hour
    hour_factor = math.sin((now.hour / 24.0) * 2 * math.pi)
    wave_height = round(profile["base_wave"] + hour_factor * 0.15 + random.uniform(-0.05, 0.05), 2)
    wave_period = round(profile["base_period"] + hour_factor * 0.2 + random.uniform(-0.1, 0.1), 1)
    wind_speed = round(profile["base_wind"] + hour_factor * 0.8 + random.uniform(-0.3, 0.3), 1)
    wind_dir = round((profile["base_dir"] + random.uniform(-3, 3)) % 360, 1)
    pressure = round(profile["base_pressure"] - hour_factor * 0.5 + random.uniform(-0.2, 0.2), 1)
    temp = round(profile["base_temp"] + hour_factor * 0.3 + random.uniform(-0.1, 0.1), 1)
    
    return {
        "source": "Hydrodynamic Simulator",
        "station_key": station_key,
        "station_id": profile["buoy_id"],
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "wave_height": max(0.4, wave_height),
        "wave_period": max(3.0, wave_period),
        "wave_direction": wind_dir,
        "wind_speed": max(1.0, wind_speed),
        "wind_direction": wind_dir,
        "pressure": pressure,
        "temperature": temp,
        "swell_wave_height": round(max(0.2, wave_height * 0.65), 2),
        "swell_wave_period": round(wave_period * 1.15, 1)
    }

def generate_historical_series(station_key: str = "chennai", hours: int = 24) -> List[Dict[str, Any]]:
    """
    Generate coherent historical metocean time-series for specified duration.
    """
    profile = STATION_PROFILES.get(station_key.lower(), STATION_PROFILES["chennai"])
    now = datetime.datetime.now()
    history = []
    
    # Step interval: 1 hour
    points = max(12, hours)
    for i in range(points, -1, -1):
        t = now - datetime.timedelta(hours=i)
        t_phase = (t.hour / 24.0) * 2 * math.pi
        macro_trend = math.sin((i / 48.0) * math.pi)
        
        # Diurnal + tidal wave cycle
        h = profile["base_wave"] + (math.sin(t_phase) * 0.3) + (macro_trend * 0.4) + random.uniform(-0.08, 0.08)
        p = profile["base_period"] + (math.sin(t_phase + 0.5) * 0.4) + random.uniform(-0.1, 0.1)
        w = profile["base_wind"] + (math.sin(t_phase) * 2.5) + random.uniform(-0.5, 0.5)
        wd = (profile["base_dir"] + math.sin(t_phase) * 15.0) % 360
        bar = profile["base_pressure"] - (math.sin(t_phase) * 1.5) + random.uniform(-0.2, 0.2)
        temp = profile["base_temp"] + (math.sin(t_phase - 1.5) * 1.2) + random.uniform(-0.1, 0.1)
        
        history.append({
            "time": t.strftime("%Y-%m-%dT%H:%M:%S"),
            "wave_height": round(max(0.4, h), 2),
            "wave_period": round(max(3.5, p), 1),
            "wind_speed": round(max(1.5, w), 1),
            "wind_direction": round(wd, 1),
            "pressure": round(bar, 1),
            "temperature": round(temp, 1)
        })
    return history
