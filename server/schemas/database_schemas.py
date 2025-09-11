from pydantic import BaseModel
from datetime import datetime, date # Importar date también
from typing import Optional
import uuid

class LLMAnswer(BaseModel):
    id: uuid.UUID
    petition: str
    timestamp_zone: datetime
    answer_text: str

    class Config:
        from_attributes = True

class UserPetition(BaseModel):
    id: uuid.UUID
    duration: Optional[int] = None
    kids_age: Optional[str] = None
    budget: Optional[str] = None
    interests: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TripOutput(BaseModel):
    id: uuid.UUID
    trip_title: Optional[str] = None
    start_date: date
    budget: Optional[str] = None
    description: Optional[str] = None
    kids_age: Optional[str] = None
    interests: Optional[str] = None
    duration: Optional[int] = None

    class Config:
        from_attributes = True