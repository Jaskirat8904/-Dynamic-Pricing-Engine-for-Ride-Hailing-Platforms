from storage.db import SessionLocal
from storage.models import PricingRecord


def save_pricing_window(data: dict):
    db = SessionLocal()
    try:
        record = PricingRecord(
            geohash=data.get("geohash"),
            demand=data.get("demand"),
            supply=data.get("supply"),
            avg_demand=data.get("avg_demand"),
            avg_supply=data.get("avg_supply"),
            alpha=data.get("alpha"),
            surge_multiplier=data.get("surge_multiplier"),
            final_price_range=data.get("final_price_range"),
            window_timestamp=data.get("window_timestamp"),
        )
        db.add(record)
        db.commit()
    finally:
        db.close()
