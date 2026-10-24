import math
from typing import Dict, Any

def compute_hydrodynamic_features(reading: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate physical oceanographic and air-sea interaction features from metocean telemetry.
    """
    hs = float(reading.get("wave_height", 1.8))
    tp = float(reading.get("wave_period", 8.5))
    wspd = float(reading.get("wind_speed", 10.0))  # in m/s
    pressure = float(reading.get("pressure", 1012.0))
    
    # 1. Approximate deep-water wavelength (lambda = g * Tp^2 / (2 * pi) approx 1.56 * Tp^2)
    wavelength = round(1.56 * (tp ** 2), 2)
    
    # 2. Wave steepness S = Hs / wavelength
    steepness = round(hs / max(10.0, wavelength), 4)
    
    # 3. Wind drag stress tau = rho_air * Cd * V^2 (rho_air approx 1.225 kg/m^3, Cd approx 0.0015)
    wind_drag = round(1.225 * 0.0015 * (wspd ** 2), 3)
    
    # 4. Wave Energy Flux Index (proportional to Hs^2 * Tp)
    energy_flux = round((hs ** 2) * tp, 2)
    
    # 5. Barometric depression (delta from standard 1013.25 hPa)
    baro_drop = max(0.0, round(1013.25 - pressure, 1))
    
    return {
        "wavelength_m": wavelength,
        "wave_steepness": steepness,
        "wind_drag_pa": wind_drag,
        "energy_flux": energy_flux,
        "baro_depression_hpa": baro_drop,
        "is_steep": steepness > 0.04
    }
