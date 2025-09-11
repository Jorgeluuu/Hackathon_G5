
# Importa la función de guardado desde tu controlador
from server.core.config import get_llm
from server.prompts.prompt import ITINERARY_PLANNER_PROMPT
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class ItineraryPlannerAgent:
    def __init__(self, model_name: str = "deepseek-r1-distill-llama-70b", resources: dict = None):
        self.llm = get_llm(model_name=model_name, provider="groq")
        self.resources = resources if resources is not None else {}

    def generate_itinerary(self, user_preferences: dict) -> str:
        prompt = self._create_prompt(user_preferences)
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            logger.error(f"Error al generar el itinerario con el LLM: {e}")
            return "Lo siento, no pude generar un itinerario en este momento."

    def _create_prompt(self, preferences: dict) -> str:
        # Aquí construirás el prompt detallado para el LLM
        # Basado en las preferencias del usuario (duración, edad de los niños, presupuesto, etc.)
        # y el objetivo del Ratoncito Pérez.

        # Formatear los recursos para incluirlos en el prompt
        festividades_str = ""
        if self.resources.get("festividades"):
            festividades_str = "Información sobre festividades en Madrid:\n"
            for festivity in self.resources["festividades"]:
                festividades_str += f"- {festivity['name']}: {festivity['description']}\n"

        links_str = ""
        if self.resources.get("links"):
            links_str = "\nEnlaces de interés sobre Madrid:\n"
            for category, urls in self.resources["links"].items():
                links_str += f"  {category}:\n"
                for url in urls:
                    links_str += f"    - {url}\n"

        madrid_destino_str = ""
        if self.resources.get("madrid_destino"):
            md_data = self.resources["madrid_destino"]
            madrid_destino_str = "\nInformación sobre Madrid Destino:\n"
            madrid_destino_str += f"  Definición: {md_data.get('definition', '')}\n"
            madrid_destino_str += "  Principales actividades:\n"
            for activity in md_data.get('main_activities', []):
                madrid_destino_str += f"    - {activity}\n"
            madrid_destino_str += "  Servicios destacados:\n"
            for service in md_data.get('featured_services', []):
                madrid_destino_str += f"    - {service}\n"
            if md_data.get('contact_info'):
                madrid_destino_str += "  Información de contacto:\n"
                for key, value in md_data['contact_info'].items():
                    madrid_destino_str += f"    - {key.replace('_', ' ').title()}: {value}\n"

        transporte_str = ""
        if self.resources.get("transporte"):
            tp_data = self.resources["transporte"]
            transporte_str = "\nInformación sobre Transporte Público en Madrid:\n"
            transporte_str += f"  Introducción: {tp_data.get('introduction', '')}\n"
            transporte_str += "  Información básica para utilizar el transporte público:\n"
            for key, value in tp_data.get('basic_info_public_transport', {}).items():
                transporte_str += f"    - {key.replace('_', ' ').title()}: {value}\n"
            transporte_str += "  Modalidades de transporte:\n"
            for modality in tp_data.get('modalities', []):
                transporte_str += f"    - {modality['name']}: {modality['description']}\n"
                for link in modality.get('links', []):
                    transporte_str += f"      Link: {link}\n"
            if tp_data.get('private_transport') and tp_data['private_transport'].get('taxi'):
                transporte_str += f"  Transporte privado (Taxi): {tp_data['private_transport']['taxi'].get('description', '')}\n"


        full_resources_info = f"{festividades_str}{links_str}{madrid_destino_str}{transporte_str}"

        return ITINERARY_PLANNER_PROMPT.format(
            duration=preferences.get('duration', 'no especificada'),
            kids_age=preferences.get('kids_age', 'no especificada'),
            budget=preferences.get('budget', 'no especificado'),
            interests=preferences.get('interests', 'ninguno'),
            resources_info=full_resources_info # Pasar la información de los recursos al prompt
        )

# Importa las funciones del controlador de base de datos.
from controllers.itinerary_controller import save_user_petition, save_itinerary

def generate_and_save_itinerary(user_input_text: str):
    """
    Función principal que procesa la petición de un usuario y guarda el itinerario.
    
    Args:
        user_input_text: El texto original que el usuario ha escrito.
    """
    
    # --- PASO 1: EXTRAER LA INFORMACIÓN CLAVE (LA "ENTRADA") ---
    # Tu tarea pendiente para configurar el agente es analizar el 'user_input_text' y extraer los datos relevantes.
    # El resultado debe ser un diccionario con las siguientes variables.
    
    print(f"Agente: Analizando la petición del usuario: '{user_input_text}'")
    
    # Aquí es donde tu modelo LLM hará su magia.
    # Por ahora, usamos datos de ejemplo:
    extracted_data = {
        "duration": 5,
        "kids_age": "5, 8",
        "budget": "medio",
        "interests": "museos, parques",
    }
    
    # --- PASO 2: GUARDAR LA ENTRADA EN LA BASE DE DATOS ---
    # Llama a la función del controlador que guarda la petición estructurada.
    # No te preocupes por el código de la función, solo llámala con los datos correctos.
    request_id = save_user_petition(extracted_data)
    
    if not request_id:
        print("Error: No se pudo guardar la petición. Abortando.")
        return None
        
    print(f"Agente: Petición guardada con ID: {request_id}")


    # --- PASO 3: GENERAR EL PLAN DE VIAJE (LA "SALIDA") ---
    # Usa la información extraída para generar el plan de viaje completo.
    # El resultado debe ser un diccionario para el viaje y una lista de diccionarios para las actividades.
    
    print("Agente: Generando el plan de viaje...")
    
    trip_plan_data = {
        "nombre_viaje": "Viaje a Madrid con Niños",
        "duration": extracted_data["duration"],
        "budget": extracted_data["budget"],
        "kids_age": extracted_data["kids_age"],
        "interests": extracted_data["interests"],
        "descripcion_viaje": "Un plan de 5 días enfocado en actividades familiares.",
    }

    activities_list = [
        {
            "nombre_actividad": "Visita al Museo del Prado",
            "lugar": "Madrid",
            "descripcion_actividad": "Tour por la colección de arte española.",
            "hora_sugerida": "mañana",
            "costo_estimado": "15€",
            "transporte_sugerido": "Metro",
        },
        {
            "nombre_actividad": "Paseo en el Parque del Retiro",
            "lugar": "Madrid",
            "descripcion_actividad": "Disfrutar de un paseo en barca en el lago.",
            "hora_sugerida": "tarde",
            "costo_estimado": "Gratis",
            "transporte_sugerido": "Caminando",
        },
    ]
    
    # --- PASO 4: GUARDAR LA SALIDA EN LA BASE DE DATOS ---
    # Llama a la función del controlador que guarda el plan final.
    # Esta función guarda los datos en las tablas 'trips' y 'activities'.
    success = save_itinerary(trip_plan_data, activities_list)
    
    if success:
        print("Agente: ¡Plan de viaje guardado con éxito!")
    else:
        print("Agente: Hubo un error al guardar el itinerario.")

# Ejemplo de uso:
# generate_and_save_itinerary("Quiero un viaje a Madrid de 5 días con mis dos hijos de 5 y 8 años, con un presupuesto medio, y nos gustan los museos y parques.")

