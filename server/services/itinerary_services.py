from datetime import datetime
from server.schemas.itinerary_schema import Itinerary, DayPlan, Activity

def generate_itinerary(planning_data: dict) -> Itinerary:
    destination = planning_data.get("destination", "Madrid")
    duration_days = int(planning_data.get("duration_days", 2))

    days = []
    for i in range(1, duration_days + 1):
        day_plan = DayPlan(
            day=i,
            activities=[
                Activity(time="10:00", activity="Visit Retiro Park", location="Parque del Retiro"),
                Activity(time="13:00", activity="Family lunch", location="Casa Botín"),
                Activity(time="16:00", activity="Museo del Prado", location="Museo del Prado"),
            ]
        )
        days.append(day_plan)

    itinerary = Itinerary(
        destination=destination,
        duration_days=duration_days,
        days=days,
        recommendations={
            "hotels": ["Hotel Ratoncito", "Magic Family Inn"],
            "transport": ["Metro", "Bus turístico"],
        }
    )
    return itinerary
