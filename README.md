# 🌊 WAVE AI
## AI-Based Coastal Wave Activity & Risk Prediction System

![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=Plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=Pandas&logoColor=white)
![ERDDAP](https://img.shields.io/badge/ERDDAP-NOAA%20CoastWatch-008080?style=for-the-badge&logo=NOAA&logoColor=white)

**WAVE AI** is a professional coastal wave activity prediction and risk monitoring platform. It collects multi-variable ocean and weather telemetry (including real-time NOAA ERDDAP buoy observations and live coastal marine wave feeds), computes hydrodynamic features (wave steepness $H_s/\lambda$, wind drag stress, barometric gradient), evaluates machine-learning risk scores (0–100), provides Explainable AI feature contributions, forecasts 12-hour forward wave trajectories, and delivers actionable maritime safety advisories.

---

## 🌊 Key Features

- **Live Real-Time Data**:
  - Ingests live telemetry from NOAA ERDDAP (`tabledap/cwwcNDBCMet.json`) for oceanic buoys (e.g. Buoy 41002, 46042).
  - Fetches sub-hourly coastal wave height, wave period, swell, wind, temp, and barometric pressure for Indian coastal stations (Chennai, Pondicherry, Nagapattinam, Kanyakumari, Visakhapatnam, Mumbai).
  - Smooth offline hydrodynamic fallback simulation ensuring zero crashes.
- **🔄 On-Demand Data Refresh**:
  - Full-width cyan button in the sidebar + page-specific refresh buttons in the top header banner.
  - Bypasses cache, pulls the latest observational data, recalculates risk and forecasts, and displays a confirmation toast with updated timestamps.
- **Pixel-Perfect Dark Marine Interface**:
  - Deep marine aesthetic (`#070d18`, `#0f1c30`), glowing state orbs (Calm/Moderate/Rough/Very Rough), and high-contrast Plotly visualizations.
- **5 Comprehensive Views**:
  1. **Dashboard**: Current ocean/weather condition cards, central Hero Risk Card, 24-hour wave trend, and XAI risk contribution factors.
  2. **Wave Analysis**: Multi-range analytical exploration (Last 24 hours, Last 3 days, Last 7 days, Last 30 days) with synchronized wave height and period charts.
  3. **Predictions**: 12-hour forward wave height trajectory with 90% confidence envelope ($\pm 1\sigma$), peak wave outlook, elevated risk window, and hourly forecast tables.
  4. **Alerts**: Hero active alert advisory card (High Wave Activity — Rough Advisory), probability & horizon metrics, and operational maritime safety rules for small craft, ports, and recreation.
  5. **About**: Mathematical oceanographic formulas, architecture diagram, and buoy registry.

---

## 🚀 Quick Start

### 1. Installation

Ensure you have Python 3.10+ installed. In the project root, install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Launch the Application

```bash
python -m streamlit run frontend/app.py
```

Open your browser at `http://localhost:8501`.

---

## 📁 Project Directory Structure

```
WAVE AI/
├── backend/
│   ├── data/
│   │   ├── erddap_client.py      # Real-time NOAA CoastWatch ERDDAP REST client
│   │   ├── marine_api_client.py  # Live sub-hourly coastal wave & weather telemetry
│   │   ├── mock_buoy_feed.py     # Hydrodynamic Pierson-Moskowitz fallback simulator
│   │   └── data_manager.py       # Central broker with caching & on-demand refresh
│   ├── preprocessing/
│   │   └── pipeline.py           # Wave steepness, wind drag, barometric gradient
│   ├── models/
│   │   └── model_loader.py       # Risk scoring, classification, 12h forecast generator
│   └── database/
│       └── db.py                 # SQLite persistence for telemetry & alert incident logs
│
├── frontend/
│   ├── app.py                    # Main Streamlit application entrypoint & router
│   ├── assets/
│   │   └── style.css             # Custom ocean dark UI styling & glowing indicators
│   ├── config/
│   │   └── config.py             # Station registry, thresholds, and app settings
│   ├── utils/
│   │   ├── constants.py          # UI color palettes and navigation items
│   │   ├── formatting.py         # Compass cardinal conversion & unit formatting
│   │   └── helpers.py            # Session state and timestamp helpers
│   ├── services/
│   │   ├── api.py                # Frontend data provider with refresh trigger
│   │   └── prediction_service.py # Inference and forecast service wrapper
│   ├── components/
│   │   ├── sidebar.py            # Location picker, status card, cyan refresh button, nav
│   │   ├── header_banner.py      # Top banner card with metadata & refresh action
│   │   ├── metric_cards.py       # 6 condition cards (Wave, Period, Wind, Temp, Pressure)
│   │   ├── risk_card.py          # Hero current wave activity card with glowing orb
│   │   ├── wave_chart.py         # Plotly charts with threshold reference dashed lines
│   │   ├── prediction_card.py    # 3 Outlook cards + 12h trajectory visualization
│   │   ├── alert_box.py          # Active alert status card + operational recommendations
│   │   └── explanation.py        # Explainable AI (XAI) feature contribution widget
│   └── pages/
│       ├── dashboard.py          # Real-time conditions & hero activity view
│       ├── wave_analysis.py      # Multi-range time-series analytics (24h/3d/7d/30d)
│       ├── predictions.py        # 12-hour predictive modeling & forecast schedule
│       ├── alerts.py             # Active marine hazards & maritime SOP rules
│       └── about.py              # Technical equations, architecture & buoy table
│
├── requirements.txt
└── README.md
```

---

## 📍 Monitored Stations Registry

1. **Chennai Coast** (Bay of Bengal, BD08 Buoy)
2. **Pondicherry Coast** (Bay of Bengal, BD09 Buoy)
3. **Nagapattinam Coast** (Bay of Bengal, BD10 Buoy)
4. **Kanyakumari Coast** (Tri-Sea Confluence, IO01 Buoy)
5. **Visakhapatnam Coast** (Deep-Water Bay, BD06 Buoy)
6. **Mumbai Coast** (Arabian Sea, AD02 Buoy)
7. **NOAA Buoy 41002** (South Hatteras, North Atlantic)
8. **NOAA Buoy 46042** (Monterey Bay, Central California Pacific)

---

## 📊 Marine Risk Classification Benchmarks

| Classification | Significant Wave Height ($H_s$) | Composite Risk Score | Advisory & Operational Impact |
| :--- | :--- | :--- | :--- |
| 🟢 **CALM** | $< 1.5\text{ m}$ | $0 - 35$ | Safe conditions for artisanal fishing, port ops, and swimming. |
| 🟡 **MODERATE** | $1.5\text{ m} - 2.5\text{ m}$ | $36 - 65$ | Noticeable swell. Small craft advisory recommended. |
| 🟠 **ROUGH** | $2.5\text{ m} - 3.5\text{ m}$ | $66 - 85$ | High wave energy. Artisanal craft restriction; harbor surge. |
| 🔴 **VERY ROUGH** | $> 3.5\text{ m}$ | $86 - 100$ | Severe sea state. Complete suspension of nearshore and fishing activity. |

---

## ⚠️ Prototype Disclaimer
> **WAVE AI** is a machine-learning research and operational prototype. Its predictions and classifications should not be treated as official marine safety warnings. Always consult national meteorological agencies (INCOIS, IMD, NOAA) for official maritime disaster alerts.
