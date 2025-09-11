from server.agents.planner_agent import ItineraryPlannerAgent
from server.agents.chat_agent import ChatAgent
from server.schemas.itinerary_schema import ItineraryRequest, ItineraryResponse, ChatRequest, ChatResponse
import logging

logger = logging.getLogger(__name__)

# Simulación de almacenamiento de preferencias de usuario por sesión
# En una aplicación real, esto sería un almacenamiento persistente asociado a un usuario/sesión
_current_user_preferences = {}

async def generate_itinerary_controller(request: ItineraryRequest, resource_data: dict) -> ItineraryResponse:
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

async def chat_with_agent_controller(request: ChatRequest, resource_data: dict) -> ChatResponse:
    """
    Controlador para manejar la interacción de chat con el agente.
    """
    global _current_user_preferences

    # Inicializar el historial de conversación si no existe
    if request.conversation_history is None:
        request.conversation_history = []

    # Manejar las preferencias del usuario
    current_preferences = _current_user_preferences.get("default_user", None) # Usamos "default_user" como clave de sesión

    if request.user_preferences:
        # Si se envían nuevas preferencias en la solicitud, actualizamos las actuales
        _current_user_preferences["default_user"] = request.user_preferences
        current_preferences = request.user_preferences
    elif current_preferences is None:
        # Si no hay preferencias en la solicitud ni en la "sesión", inicializamos con un valor por defecto
        # Esto es crucial para que el agente siempre tenga preferencias, incluso si el primer mensaje de chat no las incluye
        current_preferences = ItineraryRequest(
            duration=3,
            kids_age="0", # Sin niños por defecto
            budget="medio",
            interests="general"
        )
        _current_user_preferences["default_user"] = current_preferences


    # Añadir el mensaje del usuario al historial
    request.conversation_history.append({"role": "user", "content": request.message})

    # Instanciar el ChatAgent
    chat_agent = ChatAgent()

    agent_response_content = "Lo siento, hubo un error al procesar tu mensaje. Por favor, inténtalo de nuevo más tarde."
    try:
        # Generar la respuesta del agente usando el ChatAgent
        # Asegurarse de pasar las preferencias como un diccionario
        agent_response_content = chat_agent.generate_chat_response(
            messages=request.conversation_history,
            user_preferences=current_preferences.model_dump()
        )
    except Exception as e:
        logger.error(f"Error al generar la respuesta del chat con el agente: {e}")

    # Añadir la respuesta del agente al historial
    request.conversation_history.append({"role": "assistant", "content": agent_response_content})

    # Devolver la respuesta del agente y el historial actualizado, incluyendo las preferencias actuales
    return ChatResponse(
        response=agent_response_content,
        conversation_history=request.conversation_history,
        user_preferences=current_preferences # Devolver las preferencias actuales
    )
        