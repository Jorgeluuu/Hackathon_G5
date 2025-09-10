from pydantic import BaseModel
from typing import List, Optional

class Recommendation(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[float] = None

class RecommendationResponse(BaseModel):
    items: List[Recommendation]
