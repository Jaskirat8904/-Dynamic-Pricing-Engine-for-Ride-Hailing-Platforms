from alerts.alert_engine import generate_alerts


def test_generate_alerts_empty():
    alerts = generate_alerts(None, threshold=2.0)
    assert isinstance(alerts, list)
    assert len(alerts) == 1


def test_generate_alerts_high_surge():
    latest = {
        "geohash": "ttnfu2",
        "surge_multiplier": 2.5,
        "window_timestamp": 1779330000,
    }
    alerts = generate_alerts(latest, threshold=2.0)
    assert any(a["level"] == "high" for a in alerts)
