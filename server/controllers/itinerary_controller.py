from server.agents.planner_agent import ItineraryPlannerAgent
from server.schemas.itinerary_schema import ItineraryRequest, ItineraryResponse
import logging
# from server.main import resource_data # Importar resource_data  <-- ELIMINAR ESTA LÍNEA

logger = logging.getLogger(__name__)

async def generate_itinerary_controller(request: ItineraryRequest, resource_data: dict) -> ItineraryResponse: # <-- AÑADIR resource_data como parámetro
    """
    Controlador para generar un itinerario mágico basado en las preferencias del usuario.
    """
    # Pasar los recursos cargados al agente
    planner_agent = ItineraryPlannerAgent(resources=resource_data)
    
    user_preferences = {
        "duration": request.duration,
        "kids_age": request.kids_age,
        "budget": request.budget,
        "interests": request.interests
    }

    try:
        itinerary_content = planner_agent.generate_itinerary(user_preferences)
        return ItineraryResponse(itinerary=itinerary_content)
    except Exception as e:
        logger.error(f"Error en el controlador al generar el itinerario: {e}")
        # En un entorno de producción, podrías querer devolver un error más específico
        return ItineraryResponse(itinerary="Lo siento, hubo un error al generar el itinerario. Por favor, inténtalo de nuevo más tarde.")