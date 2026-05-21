def matching_summary(matches):
    if not matches:
        return {"total_matches": 0, "matched_riders": 0, "matched_drivers": 0}

    riders = {m.get("rider_id") for m in matches if m.get("rider_id")}
    drivers = {m.get("driver_id") for m in matches if m.get("driver_id")}

    return {
        "total_matches": len(matches),
        "matched_riders": len(riders),
        "matched_drivers": len(drivers),
    }
