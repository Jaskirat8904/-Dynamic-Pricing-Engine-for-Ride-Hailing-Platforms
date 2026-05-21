from typing import TypedDict


class RideEvent(TypedDict):
    event_id: str
    rider_id: str
    geohash: str
    event_time: int
    base_price: int
    ride_type: str


class DriverEvent(TypedDict):
    driver_id: str
    geohash: str
    status: str
    rating: float
    event_time: int


class SurgeOutput(TypedDict):
    geohash: str
    demand: int
    supply: int
    surge_multiplier: float
    final_price_range: str
    window_timestamp: int
