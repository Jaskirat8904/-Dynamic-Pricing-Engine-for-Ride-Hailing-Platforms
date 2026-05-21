from fastapi import APIRouter
from pydantic import BaseModel

from matching.matcher import match_driver_to_rider

router = APIRouter(prefix="/match", tags=["matching"])


class MatchRequest(BaseModel):
    geohash: str
    riders: list
    drivers: list
    demand_pressure: float = 1.0


@router.post("/")
def create_match(req: MatchRequest):
    result = match_driver_to_rider(
        req.riders, req.drivers, req.geohash, req.demand_pressure
    )
    return {"match": result}
