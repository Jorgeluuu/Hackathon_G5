from fastapi import HTTPException
from server.schemas.recommendations_schema import RecommendationResponse
from server.services.recommendations_service import get_recommendations

def recommendations_controller(category: str, filters: dict) -> RecommendationResponse:
    try:
        return get_recommendations(category, filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
