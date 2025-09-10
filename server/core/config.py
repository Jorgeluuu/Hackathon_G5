# Configuración (env vars)
from dotenv import load_dotenv
import os
import requests
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PlannerAgent:
    def __init__(self, groq_api_key: str, model: str = "deepseek-r1-distill-llama-70b"): # Aseguramos un modelo conocido
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables or provided.")
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def invoke(self, prompt: str) -> str:
        """
        Envía el prompt a la API de GROQ y devuelve la respuesta.
        """
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7, # Añadimos el parámetro temperature
        }

        try:
            logger.debug(f"Sending request to Groq API with model: {self.model}")
            response = requests.post(self.endpoint, headers=headers, json=data)
            response.raise_for_status()
            
            json_response = response.json()
            logger.debug(f"Groq API response: {json_response}")
            
            if "choices" not in json_response:
                raise ValueError(f"Unexpected API response format: {json_response}")
                
            return json_response["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
            raise RuntimeError(f"Error calling Groq API: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing API response: {str(e)}")
            raise

class BackupAgent:
    def __init__(self, groq_api_key: str, model: str = "mixtral-8x7b-32768"): # Aseguramos un modelo conocido
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables or provided.")
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions" # Unificamos el endpoint

    def invoke(self, prompt: str) -> str:
        """
        Envía el prompt a la API de GROQ y devuelve la respuesta.
        """
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7, # Añadimos el parámetro temperature
        }

        try:
            logger.debug(f"Sending request to Groq API with model: {self.model}")
            response = requests.post(self.endpoint, headers=headers, json=data)
            response.raise_for_status()
            
            json_response = response.json()
            logger.debug(f"Groq API response: {json_response}")
            
            if "choices" not in json_response:
                raise ValueError(f"Unexpected API response format: {json_response}")
                
            return json_response["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
            raise RuntimeError(f"Error calling Groq API: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing API response: {str(e)}")
            raise


def get_llm(model_name: str = "", provider: str = ""):
    """
    Devuelve el agente adecuado.
    - Si el proveedor es GROQ y la clave está disponible, intenta crear PlannerAgent.
    - En caso de cualquier error, devuelve BackupAgent.
    """
    if provider != "groq":
        logger.error(f"Unsupported provider: {provider}")
        raise ValueError(f"Unsupported provider: {provider}")

    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is not set.")
        # Intentamos crear el agente principal
        return PlannerAgent(groq_api_key=groq_api_key, model=model_name)
    except Exception as e:
        logger.warning(f"Fallo al inicializar PlannerAgent ({e}); usando BackupAgent.")
        # Devolvemos el agente de respaldo
        return BackupAgent(model=model_name)