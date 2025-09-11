from pydantic import BaseModel, Field
from typing import Optional, List

class ItineraryRequest(BaseModel):
    duration: int = Field(..., description="Duración de la estancia en días.")
    kids_age: str = Field(..., description="Edades de los niños (ej. '5, 8, 12').")
    budget: str = Field(..., description="Presupuesto (ej. 'bajo', 'medio', 'alto').")
    interests: Optional[str] = Field(None, description="Intereses especiales (ej. 'museos', 'parques').")

class ItineraryResponse(BaseModel):
    itinerary: str = Field(..., description="El itinerario mágico generado por el Ratoncito Pérez.")

class ChatRequest(BaseModel):
    message: str = Field(..., description="Mensaje del usuario en el chat.")
    conversation_history: Optional[List[dict]] = Field(None, description="Historial de la conversación.")
    user_preferences: Optional[ItineraryRequest] = Field(None, description="Preferencias iniciales o actualizadas del usuario.")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "¿Puedes ayudarme a planificar un día en Madrid?",
                "conversation_history": [],
                "user_preferences": {
                    "duration": 1,
                    "kids_age": "5, 8",
                    "budget": "medio",
                    "interests": "museos, parques, comida local"
                }
            }
        }

class ChatResponse(BaseModel):
    response: str = Field(..., description="Respuesta del agente en el chat.")
    conversation_history: Optional[List[dict]] = Field(None, description="Historial actualizado de la conversación.")
    user_preferences: Optional[ItineraryRequest] = Field(None, description="Preferencias actuales del usuario en la conversación.")