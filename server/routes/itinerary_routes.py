# Endpoints FastAPI
from fastapi import APIRouter, HTTPException, Depends
from server.schemas.itinerary_schema import ItineraryRequest, ItineraryResponse
from server.controllers.itinerary_controller import generate_itinerary_controller
from server.dependencies import get_resource_data # Importar desde el nuevo archivo de dependencias

router = APIRouter()

@router.post("/generate_itinerary", response_model=ItineraryResponse)
async def generate_itinerary(
    request: ItineraryRequest,
    resource_data: dict = Depends(get_resource_data)
):
    """
    Genera un itinerario mágico personalizado basado en las preferencias del usuario.
    """
    try:
        response = await generate_itinerary_controller(request, resource_data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")