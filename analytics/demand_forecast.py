import os

import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "pricing_history.db")
MODEL_PATH = os.path.join(BASE_DIR, "demand_model.joblib")
DATABASE_URL = f"sqlite:///{DB_PATH.replace(os.sep, '/')}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def train_demand_model():
    df = pd.read_sql_query("SELECT * FROM pricing_records", engine)

    if df.empty or len(df) < 20:
        print("Not enough data to train demand model.")
        return None

    df["hour"] = pd.to_datetime(df["window_timestamp"], unit="s").dt.hour
    df["dayofweek"] = pd.to_datetime(df["window_timestamp"], unit="s").dt.dayofweek

    X = df[
        ["avg_demand", "avg_supply", "alpha", "surge_multiplier", "hour", "dayofweek"]
    ]
    y = df["demand"]

    split = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    if len(X_test):
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        print(f"Validation MAE: {mae:.2f}")

    dump(model, MODEL_PATH)
    print("Demand model trained and saved.")
    return model


if __name__ == "__main__":
    train_demand_model()
