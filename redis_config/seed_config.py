import json

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

alpha_config = {
    "default_alpha": 1.5,
    "geo_alpha": {
        "ttnfu2": 2.0,
        "ttnfu8": 1.8,
        "ttnfub": 1.5,
        "ttnfuc": 1.5,
        "ttnfud": 1.2,
    },
}

base_fares = {"MINI": 80, "SEDAN": 120, "SUV": 200}

r.set("surge_config", json.dumps(alpha_config))
r.set("base_fares", json.dumps(base_fares))
r.set("default_alpha", 1.5)

print("Redis config seeded successfully")
