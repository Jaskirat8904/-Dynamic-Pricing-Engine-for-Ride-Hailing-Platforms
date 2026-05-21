# 🚗 Dynamic Pricing Engine for Ride-Hailing Platforms

> A real-time, end-to-end ride-hailing intelligence platform that ingests ride and driver events, computes zone-level surge dynamically, stores historical windows, and surfaces operational insights in an interactive multi-tab Streamlit dashboard.

---

## 📌 Overview

This project simulates a production-style ride-hailing pricing system. It streams ride and driver events, calculates surge dynamically per geohash zone, stores live and historical states, predicts demand using machine learning, and displays all operations in a professional dashboard with alerts, monitoring, matching, and exportable reports.

**Core logic:** When ride demand rises and driver availability falls in a specific zone → surge multiplier increases → final price range updates → changes are stored and visualized in real time.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔄 Real-Time Event Streaming | Kafka-based producers simulate ride requests and driver availability across geohash zones |
| ⚡ Dynamic Surge Calculation | Demand, supply, rolling averages, alpha, peak-hour multipliers, and zone pressure |
| 🗄️ Redis Live State | Low-latency current surge lookup per zone |
| 📦 SQLite Historical Storage | Time-windowed pricing records for trend analysis and reporting |
| 🤖 Demand Forecasting | scikit-learn ML model trained on historical windows to predict next-window demand |
| 🔌 FastAPI Backend | REST endpoints for live surge, latest window, and matching results |
| 📊 Streamlit Dashboard | Multi-tab UI with KPI cards, charts, alerts, matching, monitoring, and exports |
| 🚨 Alerting | Detects high surge conditions, stale data, and pipeline health issues |
| 🗺️ Matching Engine | Scores and returns best rider-driver match per geohash zone |
| 📄 Reporting | CSV and PDF exports, recent history tables, summary statistics |

---

## 🛠️ Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
- Pydantic

**Streaming & Messaging**
- Apache Kafka

**Storage**
- Redis (live state)
- SQLite (historical windows)

**Machine Learning**
- scikit-learn
- joblib

**Dashboard & Visualization**
- Streamlit
- Plotly
- pandas

**Utilities & Code Quality**
- pytest · black · isort · flake8 · fpdf

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Event Generation Layer                  │
│         ride_producer.py   driver_producer.py           │
└────────────────────────┬────────────────────────────────┘
                         │  Kafka Topics
┌────────────────────────▼────────────────────────────────┐
│               Stream Processing / Surge Engine           │
│              flink_jobs/surge_engine.py                  │
│   (demand, supply, alpha, rolling avg, peak hours)       │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
┌──────────────▼──────┐      ┌────────────▼──────────────┐
│   Redis (Live State)│      │  SQLite (Historical Store) │
│  Latest surge/zone  │      │  Time-windowed records     │
└──────────────┬──────┘      └────────────┬──────────────┘
               │                          │
┌──────────────▼──────────────────────────▼───────────────┐
│                    FastAPI Backend                        │
│         /surge/{geohash}   /window/latest   /match       │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│                  Streamlit Dashboard                      │
│  Overview · Zone Detail · Alerts · Monitoring            │
│  Matching · Reports (CSV/PDF export)                     │
└─────────────────────────────────────────────────────────┘
         │                   │                  │
  ML Demand Forecast    Alert Engine      Matching Engine
```

---

## 📁 Folder Structure

```
.
├── backend/
│   └── app.py                  # FastAPI application
├── flink_jobs/
│   ├── surge_engine.py         # Surge computation logic
│   └── redis_client.py         # Redis access helpers
├── producers/
│   ├── ride_producer.py        # Ride request event generator
│   ├── driver_producer.py      # Driver availability event generator
│   └── common/
│       ├── geohash_utils.py
│       └── kafka_config.py
├── storage/
│   ├── db.py                   # SQLite connection helpers
│   ├── init_db.py              # Database initialization
│   ├── models.py               # Schema definitions
│   └── save_record.py          # Persist pricing records
├── analytics/
│   ├── demand_forecast.py      # Train forecasting model
│   └── demand_predictor.py     # Predict from stored features
├── ml/
│   └── demand_forecast.py      # ML training logic
├── matching/
│   ├── matcher.py              # Rider-driver scoring & selection
│   ├── summary.py              # Matching summary metrics
│   └── api.py                  # Matching API route
├── observability/
│   ├── monitor.py              # Pipeline health status
│   └── kafka_lag.py            # Kafka lag monitoring
├── alerts/
│   └── alert_engine.py         # High surge & stale-data alerts
├── reports/
│   └── exporter.py             # CSV and PDF export
├── dashboard/
│   ├── app.py                  # Streamlit multi-tab dashboard
│   └── utils.py                # KPI computation helpers
├── common/
│   ├── schemas.py              # Shared schemas
│   ├── kafka_config.py         # Shared Kafka config
│   └── geohash_utils.py        # Shared geohash utilities
└── tests/
    ├── test_alerts.py
    ├── test_matching.py
    ├── test_surge_logic.py
    └── test_api.py
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Apache Kafka running locally (or via Docker)
- Redis running locally (or via Docker)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/dynamic-pricing-engine.git
cd dynamic-pricing-engine
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the database

```bash
python storage/init_db.py
```

### 4. Start Kafka & Redis

```bash
# Using Docker Compose (recommended)
docker-compose up -d kafka redis
```

### 5. Start event producers

```bash
python producers/ride_producer.py &
python producers/driver_producer.py &
```

### 6. Start the surge engine

```bash
python flink_jobs/surge_engine.py
```

### 7. Start the backend API

```bash
uvicorn backend.app:app --reload --port 8000
```

### 8. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/surge/{geohash}` | Live surge multiplier and price range for a zone |
| `GET` | `/window/latest` | Latest computed pricing window snapshot |
| `POST` | `/match` | Best rider-driver match for a given geohash zone |

### Example Response

```json
{
  "geohash": "ttnfu2",
  "surge_multiplier": 2.12,
  "final_price_range": "Rs.153 - Rs.187",
  "window_timestamp": 1779331238
}
```

---

## 📊 Dashboard Tabs

### Overview
Global KPIs (windows, avg surge, max surge, avg demand/supply), selected zone live metrics, top zones leaderboard, and pipeline health summary.

### Zone Detail
Surge trend line chart, live JSON snapshot, demand vs supply chart, alpha and rolling averages visualization.

### Alerts
High surge alerts, stale data warnings, and normal status indicators.

### Monitoring
Pipeline status, row count, latest timestamp, demand/supply/surge trend chart, and Kafka lag data.

### Matching
Best rider-driver match result, matching summary metrics, and simulated matching output.

### Reports
Recent history table, CSV download, PDF report download, and summary statistics.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Test coverage includes alert generation, matching logic, surge calculation, and API smoke tests.

---

## 📈 Key Outputs

**Live**
- Surge multiplier per geohash zone
- Final price range (min–max)
- Latest pricing window snapshot
- Auto-refreshing dashboard charts
- High-surge and stale-data alerts
- Rider-driver match results

**Stored**
- Historical windows in SQLite
- Live state in Redis
- Trained demand forecast model (`.joblib`)
- CSV and PDF report downloads

---

## 🔮 Future Work

- [ ] Map-based geohash visualization
- [ ] Real Kafka lag dashboard integration
- [ ] More realistic driver-rider matching with geospatial scoring
- [ ] Authentication and multi-user support
- [ ] Docker Compose full-stack deployment
- [ ] Cloud deployment (AWS / GCP)
- [ ] Historical backtesting for pricing strategies
- [ ] A/B testing framework for surge models
- [ ] Confidence intervals for ML predictions

---

## 📝 Resume Summary

> Built a real-time ride-hailing dynamic pricing platform using Kafka, Redis, SQLite, FastAPI, Streamlit, and scikit-learn. Implemented zone-level surge computation, demand forecasting, rider-driver matching, alerting, observability, and exportable analytics dashboards with live KPIs and historical trend visualization.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <strong>Built for learning, portfolio demonstration, and interview discussion.</strong><br/>
  If you found this useful, give it a ⭐
</div>
