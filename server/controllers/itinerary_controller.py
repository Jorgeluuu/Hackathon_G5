

from server.agents.planner_agent import ItineraryPlannerAgent
from server.agents.chat_agent import ChatAgent
from server.schemas.itinerary_schema import ItineraryRequest, ItineraryResponse, ChatRequest, ChatResponse
import logging
import json
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

_current_user_preferences = {}

async def generate_itinerary_controller(request: ItineraryRequest, resource_data: dict) -> ItineraryResponse:
    planner_agent = ItineraryPlannerAgent(resources=resource_data)

    user_preferences = {
        "destination": request.destination,
        "duration_days": request.duration_days,
        "children_ages": request.children_ages,
        "budget_range": request.budget_range,
        "interests": request.interests,
        "family_size": request.family_size,
    }

    try:
        itinerary_content = planner_agent.generate_itinerary(user_preferences)

        print(f"DEBUG: Tipo de contenido recibido de Groq: {type(itinerary_content)}")
        
        # 👇 NUEVO: Parsear el texto de Groq a JSON estructurado
        structured_itinerary = parse_groq_response_to_json(itinerary_content, request.duration_days)
        
        return ItineraryResponse(itinerary=structured_itinerary)

    except Exception as e:
        logger.error(f"Error en el controlador al generar el itinerario: {e}")
        return ItineraryResponse(itinerary={
            "error": "Lo siento, hubo un error al generar el itinerario.",
            "days": [],
            "recommendations": {}
        })

async def chat_with_agent_controller(request: ChatRequest, resource_data: dict) -> ChatResponse:
    global _current_user_preferences

    if request.conversation_history is None:
        request.conversation_history = []

    # Usar diccionario en lugar de ItineraryRequest
    current_preferences = _current_user_preferences.get("default_user", {})

    if request.user_preferences:
        _current_user_preferences["default_user"] = request.user_preferences
        current_preferences = request.user_preferences
    elif not current_preferences:
        # Valores por defecto como diccionario
        current_preferences = {
            "destination": "Madrid",
            "duration_days": 3,
            "budget_range": "medio",
            "children_ages": [],
            "interests": ["general"],
            "family_size": 2
        }
        _current_user_preferences["default_user"] = current_preferences

    request.conversation_history.append({"role": "user", "content": request.message})

    chat_agent = ChatAgent()
    agent_response_content = "Lo siento, hubo un error al procesar tu mensaje."

    try:
        agent_response_content = chat_agent.generate_chat_response(
            messages=request.conversation_history,
            user_preferences=current_preferences  # Ya es dict, no necesita .model_dump()
        )
    except Exception as e:
        logger.error(f"Error en el chat con el agente: {e}")

    request.conversation_history.append({"role": "assistant", "content": agent_response_content})

    return ChatResponse(
        response=agent_response_content,
        conversation_history=request.conversation_history,
        user_preferences=current_preferences
    )

# =============================================================================
# FUNCIONES DE PARSEO PARA GROQ (NUEVAS)
# =============================================================================

def parse_groq_response_to_json(groq_text: str, duration_days: int) -> Dict[str, Any]:
    """
    Convierte la respuesta de texto de Groq en un JSON estructurado
    que el frontend pueda entender.
    """
    print(f"DEBUG: Parseando texto de Groq, longitud: {len(groq_text)} caracteres")
    
    # Si ya es un diccionario, devolver tal cual
    if isinstance(groq_text, dict):
        return groq_text
    
    # Crear estructura base del itinerario
    itinerary = {
        "destination": "Madrid",
        "total_days": duration_days,
        "days": [],
        "recommendations": {
            "hotels": [],
            "transport_info": "Utiliza el Metro de Madrid para moverte fácilmente por la ciudad.",
            "general_tips": [
                "Lleva calzado cómodo para caminar",
                "Mantente hidratado durante el día",
                "Reserva con antelación las actividades populares"
            ]
        }
    }
    
    try:
        # Intentar extraer días usando patrones regex
        day_pattern = r"(?i)(?:Día|Dia) (\d+):(.+?)(?=(?:Día|Dia) \d+:|$)"
        days_matches = re.findall(day_pattern, groq_text, re.DOTALL)
        
        print(f"DEBUG: Encontrados {len(days_matches)} días con regex")
        
        for day_num, day_content in days_matches:
            if int(day_num) <= duration_days:  # Solo incluir días dentro de la duración
                day_data = {
                    "title": f"Día {day_num} - Aventura Mágica",
                    "description": f"Explorando Madrid - Día {day_num}",
                    "activities": extract_activities_from_day(day_content),
                    "restaurants": extract_restaurants_from_day(day_content),
                    "tip": "¡El Ratoncito Pérez te desea un día maravilloso! 🐭✨"
                }
                itinerary["days"].append(day_data)
    
    except Exception as e:
        print(f"ERROR en parseo de días: {e}")
    
    # Si no se encontraron días o son menos de los esperados, completar con días genéricos
    while len(itinerary["days"]) < duration_days:
        day_num = len(itinerary["days"]) + 1
        itinerary["days"].append({
            "title": f"Día {day_num} - Descubriendo Madrid",
            "description": f"Día {day_num} de tu aventura mágica en Madrid",
            "activities": [
                {
                    "time": "Mañana",
                    "name": "Actividad mágica",
                    "description": "Explorando los encantos de Madrid",
                    "location": "Madrid"
                },
                {
                    "time": "Tarde", 
                    "name": "Paseo familiar",
                    "description": "Disfrutando de la ciudad en familia",
                    "location": "Madrid"
                }
            ],
            "restaurants": [
                {
                    "name": "Restaurante Familiar",
                    "cuisine": "Cocina tradicional madrileña",
                    "address": "Centro de Madrid",
                    "rating": 4.2,
                    "price_range": "€€"
                }
            ],
            "tip": "¡No olvides dejar un diente bajo la almohada para el Ratoncito Pérez! 🦷"
        })
    
    # Extraer información adicional del texto
    itinerary["recommendations"]["transport_info"] = extract_transport_info(groq_text)
    itinerary["recommendations"]["general_tips"] = extract_general_tips(groq_text)
    
    print(f"DEBUG: Itinerario parseado con {len(itinerary['days'])} días")
    return itinerary

def extract_activities_from_day(day_text: str) -> List[Dict]:
    """Extrae actividades del texto de un día"""
    activities = []
    
    try:
        # Buscar actividades con diferentes patrones
        activity_patterns = [
            r"- (.+?):(.+?)(?=\n-|\n\*|\n$)",  # Patrón: - Actividad: Descripción
            r"\* (.+?):(.+?)(?=\n-|\n\*|\n$)",  # Patrón: * Actividad: Descripción
            r"• (.+?):(.+?)(?=\n-|\n\*|\n•|\n$)"  # Patrón: • Actividad: Descripción
        ]
        
        for pattern in activity_patterns:
            matches = re.findall(pattern, day_text, re.DOTALL)
            for activity_name, activity_desc in matches:
                # Limpiar el texto
                activity_name = activity_name.strip()
                activity_desc = activity_desc.strip()
                
                if activity_name and activity_desc:
                    activities.append({
                        "time": "Por determinar",
                        "name": activity_name,
                        "description": activity_desc,
                        "location": "Madrid"
                    })
    
    except Exception as e:
        print(f"ERROR extrayendo actividades: {e}")
    
    # Si no se encontraron actividades, agregar una genérica
    if not activities:
        activities.append({
            "time": "Todo el día",
            "name": "Explorar Madrid",
            "description": "Descubriendo la magia de la ciudad con la familia",
            "location": "Madrid"
        })
    
    return activities

def extract_restaurants_from_day(day_text: str) -> List[Dict]:
    """Extrae restaurantes del texto de un día"""
    restaurants = []
    
    try:
        # Buscar restaurantes mencionados
        restaurant_patterns = [
            r'Restaurante ["\'](.+?)["\']',
            r'Café ["\'](.+?)["\']', 
            r'Cafetería ["\'](.+?)["\']',
            r'\"(.+?)\" \(restaurante\)',
            r'\"(.+?)\" \(café\)'
        ]
        
        for pattern in restaurant_patterns:
            matches = re.findall(pattern, day_text, re.IGNORECASE)
            for restaurant_name in matches:
                restaurants.append({
                    "name": restaurant_name,
                    "cuisine": "Cocina local",
                    "address": "Madrid",
                    "rating": 4.0,
                    "price_range": "€€"
                })
    
    except Exception as e:
        print(f"ERROR extrayendo restaurantes: {e}")
    
    # Si no se encontraron restaurantes, agregar uno genérico
    if not restaurants:
        restaurants.append({
            "name": "Restaurante Familiar Madrid",
            "cuisine": "Cocina tradicional española",
            "address": "Centro de Madrid",
            "rating": 4.2,
            "price_range": "€€"
        })
    
    return restaurants

def extract_transport_info(text: str) -> str:
    """Extrae información de transporte del texto"""
    try:
        # Buscar sección de transporte
        transport_pattern = r"(?i)Transporte.*?:(.+?)(?=Restaurantes|Consejos|Día|$)"
        match = re.search(transport_pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"ERROR extrayendo transporte: {e}")
    
    return "Utiliza el Metro de Madrid para moverte fácilmente por la ciudad."

def extract_general_tips(text: str) -> List[str]:
    """Extrae consejos generales del texto"""
    tips = []
    
    try:
        # Buscar consejos del Ratoncito Pérez
        tips_pattern = r"(?i)Consejos del Ratoncito Pérez:(.+?)(?=Transporte|Restaurantes|$)"
        match = re.search(tips_pattern, text, re.DOTALL)
        if match:
            tips_text = match.group(1).strip()
            # Extraer tips individuales
            tip_matches = re.findall(r"- \"(.+?)\"", tips_text)
            tips.extend(tip_matches)
    except Exception as e:
        print(f"ERROR extrayendo consejos: {e}")
    
    # Tips por defecto si no se encontraron
    if not tips:
        tips = [
            "Lleva calzado cómodo para caminar por Madrid",
            "Mantente hidratado, especialmente en verano",
            "Reserva con antelación para museos populares"
        ]
    
    return tips
=======
        

# Importa el cliente de Supabase que definiste en database.py
from server.core.database import supabase

def save_user_petition(petition_data):
    """
    Guarda la petición estructurada del usuario en la tabla 'user_petitions'.
    """
    if not supabase:
        print("Error: No hay conexión a Supabase.")
        return None

    try:
        response = supabase.from_('user_petitions').insert({
            'duration': petition_data.get('duration'),
            'kids_age': petition_data.get('kids_age'),
            'budget': petition_data.get('budget'),
            'interests': petition_data.get('interests')
        }).execute()
        
        # Devuelve el ID de la fila recién insertada
        return response.data[0]['id']

    except Exception as e:
        print(f"Ocurrió un error al guardar la petición del usuario: {e}")
        return None

def save_itinerary(trip_data, activities_data):
    """
    Guarda el plan de viaje final en las tablas 'trips' y 'activities'.
    """
    if not supabase:
        print("Error: No hay conexión a Supabase.")
        return None

    try:
        # 1. Guardar la información principal del viaje
        trip_response = supabase.from_('trips').insert({
            'nombre_viaje': trip_data.get('nombre_viaje'),
            'duration': trip_data.get('duration'),
            'budget': trip_data.get('budget'),
            'kids_age': trip_data.get('kids_age'),
            'interests': trip_data.get('interests'),
            'descripcion_viaje': trip_data.get('descripcion_viaje')
        }).execute()
        
        trip_id = trip_response.data[0]['id']

        # 2. Guardar las actividades, enlazándolas al viaje
        for activity in activities_data:
            activity['trip_id'] = trip_id
        
        supabase.from_('activities').insert(activities_data).execute()

        print("Itinerario guardado con éxito.")
        return True

    except Exception as e:
        print(f"Ocurrió un error al guardar el itinerario: {e}")
        return None
