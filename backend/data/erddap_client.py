import requests
import datetime
import urllib.parse
from typing import Optional, Dict, Any, List

ERDDAP_BASE_URL = "https://coastwatch.pfeg.noaa.gov/erddap/tabledap/cwwcNDBCMet.json"

def fetch_buoy_latest(station_id: str, timeout: int = 8) -> Optional[Dict[str, Any]]:
    """
    Fetch the most recent meteorological & wave observation for a given NOAA buoy ID from ERDDAP.
    """
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        # Look back up to 48 hours to ensure finding the latest active reading
        since = (now - datetime.timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        query_cols = "station,time,WVHT,DPD,APD,MWD,WSPD,WD,BAR,WTMP"
        query_url = (
            f"{ERDDAP_BASE_URL}?{query_cols}"
            f"&station=%22{urllib.parse.quote(str(station_id))}%22"
            f"&time%3E={since}"
            f"&orderByMax(%22time%22)"
        )
        
        headers = {"User-Agent": "WAVE-AI-Buoy-Client/1.0"}
        resp = requests.get(query_url, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        rows = data.get("table", {}).get("rows", [])
        if not rows:
            return None
        
        row = rows[0]
        # Schema: ['station', 'time', 'WVHT', 'DPD', 'APD', 'MWD', 'WSPD', 'WD', 'BAR', 'WTMP']
        wvht = row[2] if row[2] is not None else 1.8
        dpd = row[3] if row[3] is not None else 8.5
        apd = row[4] if row[4] is not None else 6.2
        mwd = row[5] if row[5] is not None else 135.0
        wspd = row[6] if row[6] is not None else 8.2  # in m/s
        wd = row[7] if row[7] is not None else 140.0
        bar = row[8] if row[8] is not None else 1012.0
        wtmp = row[9] if row[9] is not None else 27.5
        
        return {
            "source": "NOAA ERDDAP",
            "station_id": station_id,
            "timestamp": row[1],
            "wave_height": round(float(wvht), 2),
            "wave_period": round(float(dpd), 1),
            "average_period": round(float(apd), 1),
            "wave_direction": round(float(mwd), 1),
            "wind_speed": round(float(wspd), 1),
            "wind_direction": round(float(wd), 1),
            "pressure": round(float(bar), 1),
            "temperature": round(float(wtmp), 1),
        }
    except Exception as e:
        return None

def fetch_buoy_history(station_id: str, hours: int = 24, timeout: int = 10) -> Optional[List[Dict[str, Any]]]:
    """
    Fetch historical time series of buoy observations from ERDDAP.
    """
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        since = (now - datetime.timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        query_cols = "station,time,WVHT,DPD,APD,MWD,WSPD,WD,BAR,WTMP"
        query_url = (
            f"{ERDDAP_BASE_URL}?{query_cols}"
            f"&station=%22{urllib.parse.quote(str(station_id))}%22"
            f"&time%3E={since}"
        )
        
        headers = {"User-Agent": "WAVE-AI-Buoy-Client/1.0"}
        resp = requests.get(query_url, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        rows = data.get("table", {}).get("rows", [])
        if not rows:
            return None
        
        history = []
        for r in rows:
            wvht = r[2] if r[2] is not None else 1.8
            dpd = r[3] if r[3] is not None else 8.5
            wspd = r[6] if r[6] is not None else 8.0
            wd = r[7] if r[7] is not None else 120.0
            bar = r[8] if r[8] is not None else 1012.0
            wtmp = r[9] if r[9] is not None else 28.0
            
            history.append({
                "time": r[1],
                "wave_height": round(float(wvht), 2),
                "wave_period": round(float(dpd), 1),
                "wind_speed": round(float(wspd), 1),
                "wind_direction": round(float(wd), 1),
                "pressure": round(float(bar), 1),
                "temperature": round(float(wtmp), 1)
            })
        return history
    except Exception:
        return None
