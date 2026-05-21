def score_driver(driver, geohash, demand_pressure=1.0):
    rating = driver.get("rating", 4.0)
    status_bonus = 1.0 if driver.get("status") == "AVAILABLE" else 0.0
    same_zone_bonus = 1.5 if driver.get("geohash") == geohash else 0.0
    return rating + status_bonus + same_zone_bonus + demand_pressure


def match_driver_to_rider(riders, drivers, geohash, demand_pressure=1.0):
    candidates = [d for d in drivers if d.get("status") == "AVAILABLE"]
    if not riders or not candidates:
        return None

    rider = riders[0]
    best_driver = sorted(
        candidates,
        key=lambda d: score_driver(d, geohash, demand_pressure),
        reverse=True,
    )[0]

    return {
        "rider_id": rider.get("rider_id"),
        "driver_id": best_driver.get("driver_id"),
        "geohash": geohash,
        "driver_rating": best_driver.get("rating", None),
    }
