import os
import sys
import time

import joblib
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from sqlalchemy import create_engine

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from alerts.alert_engine import generate_alerts
from dashboard.utils import compute_kpis
from matching.matcher import match_driver_to_rider
from matching.summary import matching_summary
from observability.kafka_lag import get_topic_lag
from observability.monitor import get_pipeline_health
from reports.exporter import build_pdf_report

st.set_page_config(page_title="Dynamic Pricing Engine", page_icon="📈", layout="wide")

BASE_DIR = ROOT_DIR
DB_PATH = os.path.join(BASE_DIR, "pricing_history.db")
MODEL_PATH = os.path.join(BASE_DIR, "demand_model.joblib")
DATABASE_URL = f"sqlite:///{DB_PATH.replace(os.sep, '/')}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

st.markdown(
    """
<style>
.block-container {padding-top: 1rem; padding-bottom: 1rem;}
[data-testid="stMetricValue"] {font-size: 1.5rem;}
div.stButton > button {
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1rem;
    font-weight: 600;
}
div.stButton > button:hover {opacity: 0.92;}
</style>
""",
    unsafe_allow_html=True,
)

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = time.time()
    st.rerun()

st.title("Dynamic Pricing Engine")
st.caption(
    "Real-time ride pricing intelligence with history, alerts, monitoring, prediction, and matching."
)


@st.cache_data(ttl=30)
def load_geohashes():
    try:
        df = pd.read_sql_query(
            "SELECT DISTINCT geohash FROM pricing_records ORDER BY geohash", engine
        )
        return df["geohash"].dropna().tolist()
    except:
        return []


@st.cache_data(ttl=30)
def load_zone_data(geohash):
    try:
        q = """
        SELECT * FROM pricing_records
        WHERE geohash = ?
        ORDER BY window_timestamp ASC
        """
        return pd.read_sql_query(q, engine, params=(geohash,))
    except:
        return pd.DataFrame()


@st.cache_data(ttl=30)
def load_top_zones():
    try:
        q = """
        SELECT
            geohash,
            COUNT(*) AS windows,
            SUM(demand) AS total_demand,
            SUM(supply) AS total_supply,
            AVG(surge_multiplier) AS avg_surge,
            MAX(window_timestamp) AS latest_ts
        FROM pricing_records
        GROUP BY geohash
        ORDER BY avg_surge DESC, total_demand DESC
        """
        return pd.read_sql_query(q, engine)
    except:
        return pd.DataFrame()


zones = load_geohashes()
if not zones:
    zones = ["ttnfu2"]

with st.sidebar:
    st.header("Controls")
    geohash = st.selectbox(
        "Select geohash", zones, index=zones.index("ttnfu2") if "ttnfu2" in zones else 0
    )
    threshold = st.slider("Alert threshold", 1.0, 5.0, 2.0, 0.05)
    st.write("Auto-refresh: 30 seconds")
    st.write(
        "Last refresh:",
        time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(st.session_state.last_refresh)
        ),
    )


def fetch_json(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None


live = fetch_json(f"http://127.0.0.1:8000/surge/{geohash}")
latest = fetch_json(f"http://127.0.0.1:8000/latest/{geohash}")
df = load_zone_data(geohash)
top_zones = load_top_zones()
health = get_pipeline_health()
alerts = generate_alerts(latest, threshold=threshold)
kpis = compute_kpis(df)

st.sidebar.write("Pipeline status:", health.get("status", "unknown"))
st.sidebar.write("Rows stored:", health.get("rows", 0))

tabs = st.tabs(
    ["Overview", "Zone Detail", "Alerts", "Monitoring", "Matching", "Reports"]
)

with tabs[0]:
    if kpis:
        a, b, c, d, e = st.columns(5)
        a.metric("Windows", kpis["windows"])
        b.metric("Avg Surge", kpis["avg_surge"])
        c.metric("Max Surge", kpis["max_surge"])
        d.metric("Avg Demand", kpis["avg_demand"])
        e.metric("Avg Supply", kpis["avg_supply"])

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Selected Zone", geohash)
    k2.metric("Live Surge", f"{live['surge_multiplier']:.2f}" if live else "NA")
    k3.metric("Latest Surge", f"{latest['surge_multiplier']:.2f}" if latest else "NA")
    k4.metric("Rows Stored", f"{len(df)}")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Global Top Zones")
        if not top_zones.empty:
            st.dataframe(top_zones.head(10), use_container_width=True, hide_index=True)
        else:
            st.info("No leaderboard data yet.")

    with col2:
        st.subheader("Pipeline Health")
        st.json(health)

with tabs[1]:
    left, right = st.columns([2, 1])
    with left:
        st.subheader("Surge Trend")
        if not df.empty:
            fig = px.line(
                df,
                x="window_timestamp",
                y="surge_multiplier",
                markers=True,
                color_discrete_sequence=["#2563eb"],
            )
            fig.update_layout(
                height=420,
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No historical data available for this zone.")

    with right:
        st.subheader("Live Snapshot")
        if latest:
            st.json(latest)
        else:
            st.warning("Latest window not available.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Demand vs Supply")
        if not df.empty:
            recent = df.tail(10)
            fig2 = px.bar(
                recent,
                x="window_timestamp",
                y=["demand", "supply"],
                barmode="group",
                color_discrete_sequence=["#10b981", "#f59e0b"],
            )
            fig2.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )
            st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.subheader("Alpha and Rolling Averages")
        if not df.empty:
            recent = df.tail(10)
            fig3 = px.line(
                recent,
                x="window_timestamp",
                y=["alpha", "avg_demand", "avg_supply"],
                markers=True,
                color_discrete_sequence=["#7c3aed", "#2563eb", "#ef4444"],
            )
            fig3.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )
            st.plotly_chart(fig3, use_container_width=True)

with tabs[2]:
    if alerts:
        for a in alerts:
            if a["level"] == "high":
                st.error(a["message"])
            elif a["level"] == "medium":
                st.warning(a["message"])
            else:
                st.info(a["message"])
    else:
        st.success("No active alerts.")

with tabs[3]:
    st.subheader("Monitoring")
    st.write("Rows stored:", health.get("rows", 0))
    st.write("Max timestamp:", health.get("max_ts", "NA"))
    st.write("Status:", health.get("status", "unknown"))
    if not df.empty:
        st.line_chart(
            df.set_index("window_timestamp")[["demand", "supply", "surge_multiplier"]]
        )

    st.subheader("Kafka Lag")
    try:
        lag_data = get_topic_lag(
            "calculated_surge", "localhost:9092", "dashboard-monitor"
        )
        if lag_data:
            st.dataframe(
                pd.DataFrame(lag_data), use_container_width=True, hide_index=True
            )
        else:
            st.info("No lag data available.")
    except Exception as e:
        st.warning(f"Kafka lag unavailable: {e}")

with tabs[4]:
    st.subheader("Matching")
    if latest:
        riders = [{"rider_id": "demo_rider_1"}]
        drivers = [
            {
                "driver_id": "demo_driver_1",
                "status": "AVAILABLE",
                "rating": 4.8,
                "geohash": geohash,
            },
            {
                "driver_id": "demo_driver_2",
                "status": "AVAILABLE",
                "rating": 4.5,
                "geohash": geohash,
            },
            {
                "driver_id": "demo_driver_3",
                "status": "ON_TRIP",
                "rating": 4.9,
                "geohash": geohash,
            },
        ]
        match = match_driver_to_rider(
            riders,
            drivers,
            geohash,
            demand_pressure=float(latest.get("surge_multiplier", 1.0)),
        )
        if match:
            st.success("Best match generated.")
            st.json(match)
            summary = matching_summary([match])
            a, b, c = st.columns(3)
            a.metric("Total Matches", summary["total_matches"])
            b.metric("Matched Riders", summary["matched_riders"])
            c.metric("Matched Drivers", summary["matched_drivers"])
        else:
            st.info("No match available.")
    else:
        st.info("Latest data unavailable for matching.")

with tabs[5]:
    st.subheader("Recent History Export")
    if not df.empty:
        show_df = df[
            [
                "window_timestamp",
                "geohash",
                "demand",
                "supply",
                "avg_demand",
                "avg_supply",
                "alpha",
                "surge_multiplier",
                "final_price_range",
            ]
        ].tail(15)
        st.dataframe(show_df, use_container_width=True, hide_index=True)

        csv = show_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download recent history CSV",
            data=csv,
            file_name=f"{geohash}_recent_history.csv",
            mime="text/csv",
        )

        pdf_bytes = build_pdf_report(
            show_df, title=f"Dynamic Pricing Report - {geohash}"
        )
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"{geohash}_report.pdf",
            mime="application/pdf",
        )

        st.subheader("Report Summary")
        st.write("Total rows:", len(df))
        st.write("Average surge:", round(df["surge_multiplier"].mean(), 2))
        st.write("Max surge:", round(df["surge_multiplier"].max(), 2))
        st.write("Latest update:", int(df["window_timestamp"].max()))
    else:
        st.info("No rows available to show.")
