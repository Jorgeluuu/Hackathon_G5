from server.schemas.recommendations_schema import RecommendationResponse, Recommendation

def get_recommendations(category: str, filters: dict) -> RecommendationResponse:
    if category == "restaurants":
        items = [
            Recommendation(name="Casa Botín", description="World's oldest restaurant", address="Calle Cuchilleros 17", rating=4.7),
            Recommendation(name="El Ratoncito Café", description="Magical family spot", address="Gran Vía 25", rating=4.5),
        ]
    elif category == "hotels":
        items = [
            Recommendation(name="Hotel Ratoncito", description="A cozy family hotel", rating=4.3),
            Recommendation(name="Magic Family Inn", description="Playrooms and family-friendly services", rating=4.6),
        ]
    else:
        items = [
            Recommendation(name="Museo del Prado", description="Spain’s most famous museum", rating=4.9),
            Recommendation(name="Parque Warner", description="Theme park with kids attractions", rating=4.4),
        ]

    return RecommendationResponse(items=items)
