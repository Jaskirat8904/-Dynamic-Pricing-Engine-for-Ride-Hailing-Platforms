<div align="center">

# 🚖 Dynamic Pricing Engine for Ride-Hailing Platforms

### Real-Time Surge Pricing • Demand Forecasting • Matching • Monitoring • Analytics

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Kafka-Streaming-black?style=for-the-badge&logo=apachekafka" />
  <img src="https://img.shields.io/badge/Redis-Live_State-red?style=for-the-badge&logo=redis" />
  <img src="https://img.shields.io/badge/SQLite-Historical_Data-003B57?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/scikit--learn-ML-orange?style=for-the-badge&logo=scikitlearn" />
</p>

---

### 📌 End-to-End Real-Time Ride-Hailing Pricing & Dispatch Intelligence Platform

</div>

---

# 📖 Overview

This project simulates a production-style ride-hailing intelligence platform where ride demand and driver availability are continuously processed to dynamically compute zone-level surge pricing.

The system combines:

- ⚡ Real-time event streaming  
- 📈 Dynamic surge pricing  
- 🧠 Machine learning forecasting  
- 🚦 Rider-driver matching  
- 📊 Live operational dashboards  
- 🔔 Alerting & monitoring  
- 🗄 Historical analytics  
- 📄 Exportable reporting  

into a unified streaming data platform.

---

# ✨ Features

<table>
<tr>
<td width="50%">

## 🚘 Real-Time Event Generation
- Simulated ride events
- Simulated driver availability
- Geohash-based traffic zones
- Continuous Kafka streams

</td>
<td width="50%">

## 📈 Dynamic Surge Pricing
- Demand vs supply analysis
- Rolling averages
- Peak-hour multipliers
- Real-time fare adjustments

</td>
</tr>

<tr>
<td width="50%">

## ⚡ Redis Live State
- Low-latency pricing access
- Fast dashboard updates
- Live zone surge retrieval

</td>
<td width="50%">

## 🗄 SQLite Historical Storage
- Time-window persistence
- Historical analytics
- Reporting support
- ML training datasets

</td>
</tr>

<tr>
<td width="50%">

## 🧠 Demand Forecasting
- scikit-learn integration
- Demand prediction
- Historical trend learning
- Forecast-ready pipeline

</td>
<td width="50%">

## 🚦 Matching Engine
- Driver scoring
- Rider-driver assignment
- Dispatch simulation
- Zone-aware matching

</td>
</tr>

<tr>
<td width="50%">

## 📊 Interactive Dashboard
- KPI cards
- Trend visualizations
- Monitoring tabs
- Alerts & exports

</td>
<td width="50%">

## 🔔 Observability & Alerts
- High surge alerts
- Pipeline monitoring
- Stale data detection
- Health status tracking

</td>
</tr>
</table>

---

# 🏗 System Architecture

```text
 Ride Events + Driver Events
              │
              ▼
        Kafka Producers
              │
              ▼
     Real-Time Surge Engine
              │
      ┌───────┴────────┐
      │                │
      ▼                ▼
 Redis Live State   SQLite History
      │                │
      └───────┬────────┘
              ▼
          FastAPI
              │
              ▼
     Streamlit Dashboard
              │
 ┌────────────┼────────────┐
 ▼            ▼            ▼
ML       Monitoring      Alerts
```

---

# 🛠 Tech Stack

<div align="center">

| Category | Technologies |
|---|---|
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Streaming** | Apache Kafka |
| **Storage** | Redis, SQLite |
| **Machine Learning** | scikit-learn, joblib |
| **Dashboard** | Streamlit, Plotly, pandas |
| **Testing** | pytest |
| **Utilities** | black, isort, flake8, fpdf |

</div>

---

# 📂 Project Structure

```bash
dynamic_pricing_engine/
│
├── backend/
│   └── app.py
│
├── flink_jobs/
│   ├── surge_engine.py
│   └── redis_client.py
│
├── producers/
│   ├── ride_producer.py
│   ├── driver_producer.py
│   └── common/
│
├── storage/
│   ├── db.py
│   ├── init_db.py
│   ├── models.py
│   └── save_record.py
│
├── analytics/
│   ├── demand_forecast.py
│   └── demand_predictor.py
│
├── matching/
│   ├── matcher.py
│   ├── summary.py
│   └── api.py
│
├── observability/
│   ├── monitor.py
│   └── kafka_lag.py
│
├── alerts/
│   └── alert_engine.py
│
├── reports/
│   └── exporter.py
│
├── dashboard/
│   ├── app.py
│   └── utils.py
│
├── tests/
│   ├── test_alerts.py
│   ├── test_matching.py
│   ├── test_surge_logic.py
│   └── test_api.py
│
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/dynamic-pricing-engine.git

cd dynamic-pricing-engine
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Infrastructure Setup

## Start Redis

```bash
docker run -p 6379:6379 redis
```

---

## Start Kafka

```bash
docker compose up -d
```

---

# 🗄 Initialize Database

```bash
python -m storage.init_db
```

---

# ▶ Running the Platform

## 1️⃣ Start Ride Producer

```bash
python producers/ride_producer.py
```

---

## 2️⃣ Start Driver Producer

```bash
python producers/driver_producer.py
```

---

## 3️⃣ Start Surge Engine

```bash
python flink_jobs/surge_engine.py
```

---

## 4️⃣ Start FastAPI Backend

```bash
uvicorn backend.app:app --reload
```

### Backend URL

```text
http://127.0.0.1:8000
```

### Swagger Docs

```text
http://127.0.0.1:8000/docs
```

---

## 5️⃣ Start Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

### Dashboard URL

```text
http://localhost:8501
```

---

# 🔌 API Endpoints

## 📍 Get Live Surge

```http
GET /pricing/{geohash}
```

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

## 📍 Get Latest Window

```http
GET /latest
```

---

## 📍 Rider-Driver Match

```http
POST /match
```

---

# 📊 Dashboard Features

<table>
<tr>
<td width="50%">

## 📈 Overview Tab
- Global KPIs
- Top zones
- Live surge metrics
- Pipeline health

</td>
<td width="50%">

## 📉 Zone Detail Tab
- Surge trends
- Demand vs supply
- Rolling averages
- Live snapshots

</td>
</tr>

<tr>
<td width="50%">

## 🚨 Alerts Tab
- High surge alerts
- Stale data warnings
- Monitoring notifications

</td>
<td width="50%">

## 🖥 Monitoring Tab
- Pipeline status
- Time-series analytics
- Kafka lag metrics

</td>
</tr>

<tr>
<td width="50%">

## 🚦 Matching Tab
- Best-driver selection
- Dispatch simulation
- Match scoring

</td>
<td width="50%">

## 📄 Reports Tab
- CSV export
- PDF reports
- Historical analytics

</td>
</tr>
</table>

---

# 🧠 Machine Learning Pipeline

The project includes a forecasting pipeline trained on historical pricing windows.

### ML Capabilities
- Demand forecasting
- Feature engineering
- Historical trend learning
- Serialized prediction model
- Reusable analytics pipeline

### Libraries Used
- scikit-learn
- joblib

---

# 🧪 Testing

## Run All Tests

```bash
pytest
```

---

## Run Individual Tests

```bash
pytest tests/test_alerts.py

pytest tests/test_matching.py

pytest tests/test_surge_logic.py

pytest tests/test_api.py
```

---

# 📈 Example Surge Logic

```text
High Demand + Low Supply
            │
            ▼
     Higher Surge Multiplier
            │
            ▼
       Increased Ride Price
```

---

# 📦 Example Output

```json
{
  "geohash": "ttnfu2",
  "surge_multiplier": 2.12,
  "final_price_range": "Rs.153 - Rs.187",
  "window_timestamp": 1779331238
}
```

---

# 🚀 Future Improvements

- 🗺 Map-based geohash visualization
- ☁ Cloud deployment
- 🐳 Full Docker orchestration
- ☸ Kubernetes deployment
- 🔐 Authentication & RBAC
- 📊 Real Kafka lag monitoring
- 🧪 A/B pricing experiments
- 📈 Historical backtesting
- 🤖 Reinforcement learning pricing

---

# 📜 License

This project is licensed under the **MIT License**.

---

<div align="center">

# ⭐ Dynamic Pricing Engine for Ride-Hailing Platforms

### Real-Time Pricing • Streaming Analytics • Forecasting • Monitoring • Matching

</div>
