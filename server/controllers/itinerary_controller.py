from fastapi import APIRouter, HTTPException
from server.schemas.itinerary_schema import Itinerary
from server.services.itinerary_services import generate_itinerary

def create_itinerary_controller(planning_data: dict) -> Itinerary:
    try:
        return generate_itinerary(planning_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
