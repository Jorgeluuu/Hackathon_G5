from fastapi import APIRouter
from server.controllers.itinerary_controller import create_itinerary_controller
from server.schemas.itinerary_schema import Itinerary

router = APIRouter()

@router.post("/generate", response_model=Itinerary)
async def generate_itinerary(planning_data: dict):
    return create_itinerary_controller(planning_data)
