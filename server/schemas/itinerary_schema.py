from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ItineraryRequest(BaseModel):
    destination: str = Field(..., description="Destino del itinerario.")
    duration_days: int = Field(..., description="Duración en días.")
    budget_range: str = Field(..., description="Rango de presupuesto (bajo, medio, alto).")
    children_ages: Optional[List[int]] = Field([], description="Edades de los niños.")
    interests: Optional[List[str]] = Field([], description="Lista de intereses.")
    family_size: Optional[int] = Field(2, description="Tamaño de la familia (adultos + niños).")

class ItineraryResponse(BaseModel):
    itinerary: Dict[str, Any] = Field(..., description="Itinerario mágico generado.")


class ChatRequest(BaseModel):
    message: str = Field(..., description="Mensaje del usuario en el chat.")
    conversation_history: Optional[List[dict]] = Field([], description="Historial de la conversación.")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="Preferencias del usuario.")  # Cambiado a Dict

    class Config:
        json_schema_extra = {
            "example": {
                "message": "¿Puedes ayudarme a planificar un día en Madrid?",
                "conversation_history": [],
                "user_preferences": {
                    "destination": "Madrid",
                    "duration_days": 3,
                    "budget_range": "medio",
                    "children_ages": [5, 8],
                    "interests": ["museos", "parques"],
                    "family_size": 4
                }
            }
        }

class ChatResponse(BaseModel):
    response: str = Field(..., description="Respuesta del agente en el chat.")
    conversation_history: Optional[List[dict]] = Field([], description="Historial actualizado de la conversación.")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="Preferencias actuales del usuario.")  # Cambiado a Dict