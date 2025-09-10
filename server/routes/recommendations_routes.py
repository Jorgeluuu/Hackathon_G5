from fastapi import APIRouter
from server.schemas.recommendations_schema import RecommendationResponse

router = APIRouter()

@router.get("/{category}", response_model=RecommendationResponse)
def get_recommendations(category: str):
    return RecommendationResponse(
        category=category,
        items=["Example 1", "Example 2"]
    )
