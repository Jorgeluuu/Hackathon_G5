from pydantic import BaseModel
from typing import List, Optional

class Activity(BaseModel):
    time: str
    activity: str
    location: str
    tips: Optional[str] = None

class DayPlan(BaseModel):
    day: int
    activities: List[Activity]

class Itinerary(BaseModel):
    destination: str
    duration_days: int
    days: List[DayPlan]
    recommendations: dict
