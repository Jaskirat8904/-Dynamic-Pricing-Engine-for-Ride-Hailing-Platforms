from datetime import datetime

import numpy as np
import pandas as pd
import redis
from sklearn.ensemble import RandomForestRegressor

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def create_sample_demand_data():
    data = []
    for _ in range(1000):
        data.append(
            {
                "hour": np.random.randint(0, 24),
                "day_of_week": np.random.randint(0, 7),
                "geohash": np.random.choice(
                    ["ttnfu2", "ttnfu8", "ttnfub", "ttnfuc", "ttnfud"]
                ),
                "demand_count": np.random.randint(10, 100),
            }
        )
    return pd.DataFrame(data)


def train_demand_forecaster(df):
    X = df[["hour", "day_of_week"]]
    y = df["demand_count"]
    model = RandomForestRegressor(n_estimators=100, n_jobs=-1)
    model.fit(X, y)
    return model


def predict_optimal_alpha(model, current_hour, current_weekday):
    pred = model.predict([[current_hour, current_weekday]])
    predicted_demand = pred[0]
    alpha = max(1.0, min(5.0, predicted_demand / 50.0))
    return alpha, predicted_demand


if __name__ == "__main__":
    print("Training demand forecaster with synthetic data...")
    df = create_sample_demand_data()
    model = train_demand_forecaster(df)

    current_hour = datetime.now().hour
    current_weekday = datetime.now().weekday()
    alpha, demand = predict_optimal_alpha(model, current_hour, current_weekday)

    print(f"Predicted demand: {demand:.2f}")
    print(f"Optimal alpha: {alpha:.2f}")

    r.set("optimal_alpha", alpha)
    print("Updated Redis with new optimal_alpha.")
