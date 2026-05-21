import os

import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "pricing_history.db")
DATABASE_URL = f"sqlite:///{DB_PATH.replace(os.sep, '/')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def train_demand_model():
    df = pd.read_sql_query("SELECT * FROM pricing_records", engine)

    if df.empty or len(df) < 10:
        print("Not enough data to train demand model.")
        return None

    df = df.dropna()
    X = df[["avg_demand", "avg_supply", "alpha", "surge_multiplier"]]
    y = df["demand"]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    dump(model, os.path.join(BASE_DIR, "demand_model.joblib"))
    print("Demand model trained and saved.")
    return model


if __name__ == "__main__":
    train_demand_model()
