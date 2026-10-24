from typing import Dict, Any
from backend.models.model_loader import evaluate_risk, generate_12h_trajectory, get_coastal_alerts

def predict_wave_activity(reading: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate wave risk classification and 0 - 100 risk index.
    """
    return evaluate_risk(reading)

def get_12h_forecast(reading: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate 12-hour forward wave height trajectory and peak outlook.
    """
    return generate_12h_trajectory(reading)

def get_active_alerts(reading: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate active coastal alerts and operational safety advisories.
    """
    return get_coastal_alerts(reading)
