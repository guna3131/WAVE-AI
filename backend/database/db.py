import sqlite3
import datetime
import os
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "wave_ai.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_key TEXT,
            station_name TEXT,
            wave_height REAL,
            wave_period REAL,
            wind_speed REAL,
            pressure REAL,
            temperature REAL,
            risk_score INTEGER,
            classification TEXT,
            source TEXT,
            recorded_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alert_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_name TEXT,
            alert_title TEXT,
            risk_score INTEGER,
            wave_height REAL,
            advisory_note TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_telemetry(data: Dict[str, Any], risk_info: Dict[str, Any]):
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO telemetry_logs 
            (station_key, station_name, wave_height, wave_period, wind_speed, pressure, temperature, risk_score, classification, source, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("station_key", ""),
            data.get("station_name", ""),
            data.get("wave_height", 0.0),
            data.get("wave_period", 0.0),
            data.get("wind_speed", 0.0),
            data.get("pressure", 0.0),
            data.get("temperature", 0.0),
            risk_info.get("risk_score", 0),
            risk_info.get("classification", "CALM"),
            data.get("source", "Unknown"),
            datetime.datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_recent_alert_logs(limit: int = 10) -> List[Dict[str, Any]]:
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alert_logs ORDER BY id DESC LIMIT ?", (limit,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows
    except Exception:
        return []
