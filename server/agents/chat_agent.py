from groq import Groq
import os
from typing import List, Optional
import logging
from dotenv import load_dotenv
import json # Asegúrate de que json esté importado

load_dotenv()
# Elimina la importación duplicada de logging si existe
# import logging 

logger = logging.getLogger(__name__)

class ChatAgent:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY no está configurada en las variables de entorno.")
        self.client = Groq(api_key=self.api_key)
        self.model_name = "gemma2-9b-it" # Define el modelo aquí o cárgalo desde una configuración

    def generate_chat_response(self, messages: List[dict], user_preferences: Optional[dict] = None) -> str:
        """
        Genera una respuesta de chat utilizando el modelo de lenguaje de Groq.
        """
        # Asegurarse de que user_preferences sea un diccionario para la serialización JSON
        if user_preferences is None:
            user_preferences = {}

        # Construir el mensaje del sistema con las preferencias del usuario
        system_message_content = (
            "Eres un asistente de IA útil y amigable. "
            "Tu objetivo es ayudar a los usuarios a planificar itinerarios de viaje. "
            "Considera las siguientes preferencias del usuario al generar tus respuestas: "
            f"Duración: {user_preferences.get('duration', 'no especificada')} días, "
            f"Edades de los niños: {user_preferences.get('kids_age', 'no especificada')}, "
            f"Presupuesto: {user_preferences.get('budget', 'no especificado')}, "
            f"Intereses: {user_preferences.get('interests', 'no especificados')}. "
            "Responde siempre en español." # Añadido para asegurar la respuesta en español
        )

        # Prepend the system message to the messages list
        full_messages = [{"role": "system", "content": system_message_content}] + messages

        # Filtrar mensajes inválidos (sin 'role' o 'content')
        valid_messages = []
        for msg in full_messages:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                valid_messages.append(msg)
            elif hasattr(msg, 'model_dump'): # Si es un modelo Pydantic, convertirlo a dict
                dumped_msg = msg.model_dump()
                if "role" in dumped_msg and "content" in dumped_msg:
                    valid_messages.append(dumped_msg)
                else:
                    logger.warning(f"Mensaje Pydantic mal formado (faltan 'role' o 'content'): {dumped_msg}")
            else:
                logger.warning(f"Mensaje mal formado (no es un diccionario o Pydantic, o faltan 'role' o 'content'): {msg}")

        if not valid_messages:
            logger.error("No hay mensajes válidos para enviar a la API de Groq.")
            return "Lo siento, no pude procesar tu solicitud debido a un problema con los mensajes."

        try:
            logger.debug(f"Payload enviado a Groq: {json.dumps(valid_messages, indent=2)}")

            chat_completion = self.client.chat.completions.create(
                messages=valid_messages, # Usar valid_messages aquí
                model=self.model_name, # Usar self.model_name
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error al llamar a la API de Groq: {e}")
            return "Lo siento, no pude generar una respuesta en este momento."