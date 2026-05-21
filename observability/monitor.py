import os

import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "pricing_history.db")
DATABASE_URL = f"sqlite:///{DB_PATH.replace(os.sep, '/')}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_pipeline_health():
    try:
        df = pd.read_sql_query(
            "SELECT MAX(window_timestamp) as max_ts, COUNT(*) as rows FROM pricing_records",
            engine,
        )
        rows = int(df.loc[0, "rows"])
        max_ts = int(df.loc[0, "max_ts"]) if pd.notna(df.loc[0, "max_ts"]) else None
        return {
            "rows": rows,
            "max_ts": max_ts,
            "status": "healthy" if rows > 0 else "no_data",
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
