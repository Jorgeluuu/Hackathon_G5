from pydantic import BaseModel, Field
from typing import Optional

class ItineraryRequest(BaseModel):
    duration: int = Field(..., description="Duración de la estancia en días.")
    kids_age: str = Field(..., description="Edades de los niños (ej. '5, 8, 12').")
    budget: str = Field(..., description="Presupuesto (ej. 'bajo', 'medio', 'alto').")
    interests: Optional[str] = Field(None, description="Intereses especiales (ej. 'museos', 'parques').")

class ItineraryResponse(BaseModel):
    itinerary: str = Field(..., description="El itinerario mágico generado por el Ratoncito Pérez.")