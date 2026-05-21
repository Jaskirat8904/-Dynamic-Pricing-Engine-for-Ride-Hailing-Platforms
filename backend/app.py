import json

import redis
from fastapi import FastAPI

from matching.api import router as matching_router

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.get("/surge/{geohash}")
def get_surge(geohash: str):
    val = r.get(f"surge:{geohash}")
    if val is None:
        return {
            "geohash": geohash,
            "surge_multiplier": 1.0,
            "final_price_range": "Rs.150 - Rs.150",
        }

    surge = float(val)
    return {
        "geohash": geohash,
        "surge_multiplier": surge,
        "final_price_range": f"Rs.{int(150 * surge * 0.9)} - Rs.{int(150 * surge * 1.1)}",
    }


@app.get("/latest/{geohash}")
def latest_window(geohash: str):
    data = r.get(f"latest_window:{geohash}")
    return json.loads(data) if data else {}
