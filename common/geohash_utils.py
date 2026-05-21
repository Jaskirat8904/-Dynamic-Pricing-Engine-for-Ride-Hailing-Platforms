import datetime
import random

HOT_ZONES = ["ttnfu2", "ttnfu8", "ttnfub", "ttnfuc", "ttnfud"]


def generate_random_geohash():
    hour = datetime.datetime.now().hour
    is_peak = 7 <= hour <= 10 or 17 <= hour <= 21
    weights = (
        [0.35, 0.30, 0.15, 0.12, 0.08] if is_peak else [0.20, 0.20, 0.20, 0.20, 0.20]
    )
    return random.choices(HOT_ZONES, weights=weights, k=1)[0]


def get_sleep_interval():
    hour = datetime.datetime.now().hour
    is_peak = 7 <= hour <= 10 or 17 <= hour <= 21
    return 0.3 if is_peak else 1.0
