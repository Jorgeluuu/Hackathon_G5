from typing import Dict, Any
from supabase import Client
from server.core.database import init_db
from server.schemas.database_schemas import LLMAnswer, UserPetition, TripOutput # Añadir TripOutput
import logging

logger = logging.getLogger(__name__)

async def save_llm_answer(answer: LLMAnswer) -> Dict[str, Any]:
    """
    Guarda una respuesta del LLM en la tabla 'llm_answers'.
    """
    supabase: Client = init_db()
    try:
        data, count = await supabase.from_('llm_answers').insert(answer.model_dump()).execute()
        logger.info(f"Respuesta del LLM guardada: {data}")
        return data
    except Exception as e:
        logger.error(f"Error al guardar la respuesta del LLM: {e}")
        raise

async def save_user_petition(petition: UserPetition) -> Dict[str, Any]:
    """
    Guarda una petición de usuario en la tabla 'user_petitions'.
    """
    supabase: Client = init_db()
    try:
        data, count = await supabase.from_('user_petitions').insert(petition.model_dump()).execute()
        logger.info(f"Petición de usuario guardada: {data}")
        return data
    except Exception as e:
        logger.error(f"Error al guardar la petición de usuario: {e}")
        raise

async def save_trip_output(trip: TripOutput) -> Dict[str, Any]:
    """
    Guarda un itinerario generado en la tabla 'trips_output'.
    """
    supabase: Client = init_db()
    try:
        data, count = await supabase.from_('trips_output').insert(trip.model_dump()).execute()
        logger.info(f"Itinerario guardado: {data}")
        return data
    except Exception as e:
        logger.error(f"Error al guardar el itinerario: {e}")
        raise