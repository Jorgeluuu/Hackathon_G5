from fastapi import APIRouter, Query
from server.controllers.recommendations_controller import recommendations_controller
from server.schemas.recommendations_schema import RecommendationResponse

router = APIRouter()

@router.get("/{category}", response_model=RecommendationResponse)
async def get_recommendations(category: str, filters: dict = Query(None)):
    return recommendations_controller(category, filters or {})
