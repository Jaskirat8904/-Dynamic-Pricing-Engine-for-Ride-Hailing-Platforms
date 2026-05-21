from matching.matcher import match_driver_to_rider


def test_match_driver_to_rider():
    riders = [{"rider_id": "r1"}]
    drivers = [
        {"driver_id": "d1", "status": "AVAILABLE", "rating": 4.2, "geohash": "ttnfu2"},
        {"driver_id": "d2", "status": "AVAILABLE", "rating": 4.8, "geohash": "ttnfu2"},
    ]
    result = match_driver_to_rider(riders, drivers, "ttnfu2", demand_pressure=1.5)
    assert result is not None
    assert result["driver_id"] == "d2"
