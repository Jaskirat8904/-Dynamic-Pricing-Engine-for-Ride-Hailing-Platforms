from datetime import datetime, timezone


def generate_alerts(latest_window, threshold=2.0):
    alerts = []

    if not latest_window:
        alerts.append(
            {"level": "warning", "message": "No latest window data available."}
        )
        return alerts

    surge = latest_window.get("surge_multiplier", 0)
    geohash = latest_window.get("geohash", "unknown")
    ts = latest_window.get("window_timestamp")

    if surge >= threshold:
        alerts.append(
            {"level": "high", "message": f"High surge in {geohash}: {surge:.2f}"}
        )

    if ts:
        age_seconds = int(datetime.now(timezone.utc).timestamp()) - int(ts)
        if age_seconds > 180:
            alerts.append(
                {
                    "level": "medium",
                    "message": f"Stale data for {geohash}: last update {age_seconds}s ago",
                }
            )

    return alerts
