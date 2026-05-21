from sqlalchemy import Column, Float, Integer, String

from storage.db import Base


class PricingRecord(Base):
    __tablename__ = "pricing_records"

    id = Column(Integer, primary_key=True, index=True)
    geohash = Column(String, index=True)
    demand = Column(Integer)
    supply = Column(Integer)
    avg_demand = Column(Float)
    avg_supply = Column(Float)
    alpha = Column(Float)
    surge_multiplier = Column(Float)
    final_price_range = Column(String)
    window_timestamp = Column(Integer)
