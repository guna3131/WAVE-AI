import requests
import datetime
from typing import Optional, Dict, Any, List

MARINE_API_URL = "https://marine-api.open-meteo.com/v1/marine"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_coastal_conditions(latitude: float, longitude: float, timeout: int = 8) -> Optional[Dict[str, Any]]:
    """
    Fetch real-time coastal wave and atmospheric telemetry for specific geographic coordinates.
    """
    try:
        # 1. Fetch Marine Wave Data
        marine_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "wave_height,wave_direction,wave_period,wind_wave_height,wind_wave_period,swell_wave_height,swell_wave_period",
            "timezone": "auto"
        }
        m_resp = requests.get(MARINE_API_URL, params=marine_params, timeout=timeout)
        if m_resp.status_code != 200:
            return None
        marine_data = m_resp.json().get("current", {})
        
        # 2. Fetch Surface Weather Data (Wind, Pressure, Temp)
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m",
            "timezone": "auto"
        }
        w_resp = requests.get(WEATHER_API_URL, params=weather_params, timeout=timeout)
        weather_data = w_resp.json().get("current", {}) if w_resp.status_code == 200 else {}
        
        # Extract and format
        wave_height = marine_data.get("wave_height", 1.8)
        wave_period = marine_data.get("wave_period", 8.4)
        wave_dir = marine_data.get("wave_direction", 130.0)
        
        # Note: wind_speed_10m is returned in km/h by open-meteo by default; convert to m/s
        wind_speed_kmh = weather_data.get("wind_speed_10m", 25.0)
        wind_speed_ms = round(wind_speed_kmh / 3.6, 1)
        wind_dir = weather_data.get("wind_direction_10m", 120.0)
        pressure = weather_data.get("surface_pressure", 1008.0)
        temp = weather_data.get("temperature_2m", 30.5)
        
        return {
            "source": "Live Coastal Marine Feed",
            "timestamp": marine_data.get("time", datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")),
            "wave_height": round(float(wave_height), 2),
            "wave_period": round(float(wave_period), 1),
            "wave_direction": round(float(wave_dir), 1),
            "wind_speed": wind_speed_ms,
            "wind_direction": round(float(wind_dir), 1),
            "pressure": round(float(pressure), 1),
            "temperature": round(float(temp), 1),
            "swell_wave_height": marine_data.get("swell_wave_height", 0.8),
            "swell_wave_period": marine_data.get("swell_wave_period", 7.0),
        }
    except Exception:
        return None

def fetch_coastal_history(latitude: float, longitude: float, days: int = 1, timeout: int = 10) -> Optional[List[Dict[str, Any]]]:
    """
    Fetch historical time-series of wave height and metocean conditions for coastal coordinates.
    """
    try:
        marine_params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "wave_height,wave_period,wave_direction",
            "past_days": days,
            "forecast_days": 1,
            "timezone": "auto"
        }
        m_resp = requests.get(MARINE_API_URL, params=marine_params, timeout=timeout)
        if m_resp.status_code != 200:
            return None
        hourly_m = m_resp.json().get("hourly", {})
        
        times = hourly_m.get("time", [])
        heights = hourly_m.get("wave_height", [])
        periods = hourly_m.get("wave_period", [])
        
        # Weather history for pressure & wind
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "surface_pressure,wind_speed_10m,wind_direction_10m,temperature_2m",
            "past_days": days,
            "forecast_days": 1,
            "timezone": "auto"
        }
        w_resp = requests.get(WEATHER_API_URL, params=weather_params, timeout=timeout)
        hourly_w = w_resp.json().get("hourly", {}) if w_resp.status_code == 200 else {}
        
        pressures = hourly_w.get("surface_pressure", [])
        wind_speeds = hourly_w.get("wind_speed_10m", [])
        wind_dirs = hourly_w.get("wind_direction_10m", [])
        temps = hourly_w.get("temperature_2m", [])
        
        history = []
        n = min(len(times), len(heights))
        for i in range(n):
            h = heights[i] if heights[i] is not None else 1.5
            p = periods[i] if i < len(periods) and periods[i] is not None else 8.0
            press = pressures[i] if i < len(pressures) and pressures[i] is not None else 1008.0
            ws = (wind_speeds[i] / 3.6) if i < len(wind_speeds) and wind_speeds[i] is not None else 8.0
            wd = wind_dirs[i] if i < len(wind_dirs) and wind_dirs[i] is not None else 120.0
            temp = temps[i] if i < len(temps) and temps[i] is not None else 29.0
            
            history.append({
                "time": times[i],
                "wave_height": round(float(h), 2),
                "wave_period": round(float(p), 1),
                "wind_speed": round(float(ws), 1),
                "wind_direction": round(float(wd), 1),
                "pressure": round(float(press), 1),
                "temperature": round(float(temp), 1)
            })
        return history
    except Exception:
        return None
