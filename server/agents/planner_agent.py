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