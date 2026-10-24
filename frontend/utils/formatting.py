"""
WAVE AI - Numeric, Datetime, Compass, Badge, and Safe HTML Rendering Utilities.
"""
import textwrap
import re
import streamlit as st

def render_html(html_str: str):
    """
    Renders HTML safely without triggering CommonMark code block formatting.
    Dedents all lines, removes internal blank lines, and strips outer whitespace.
    """
    cleaned = textwrap.dedent(html_str).strip()
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
    st.markdown(cleaned, unsafe_allow_html=True)

def degrees_to_compass(deg: float) -> str:
    """
    Convert meteorological degrees (0-360) into 16-point compass direction.
    E.g. 121 deg -> ESE
    """
    cardinals = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    idx = int((deg + 11.25) / 22.5) % 16
    return cardinals[idx]

def format_wave_height(val: float) -> str:
    return f"{float(val):.1f} m"

def format_period(val: float) -> str:
    return f"{float(val):.1f} s"

def format_wind_speed(val: float) -> str:
    return f"{float(val):.1f} m/s"

def format_pressure(val: float) -> str:
    return f"{int(round(float(val)))} hPa"

def format_temperature(val: float) -> str:
    return f"{float(val):.1f} °C"

def get_risk_badge_html(category: str) -> str:
    cat = category.upper()
    bg_color = {
        "CALM": "#10b981",
        "MODERATE": "#f59e0b",
        "ROUGH": "#f97316",
        "VERY ROUGH": "#ef4444"
    }.get(cat, "#00d2ff")
    
    return f'<span style="background-color: {bg_color}22; color: {bg_color}; border: 1px solid {bg_color}55; padding: 3px 10px; border-radius: 9999px; font-weight: 700; font-size: 0.82rem; letter-spacing: 0.05em;">{cat}</span>'
