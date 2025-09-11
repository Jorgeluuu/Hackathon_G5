#conexion a supabase o firebase

import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

# Carga las variables del archivo .env
load_dotenv()

# Obtener las variables de entorno para las claves
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# Variable global para almacenar la instancia del cliente Supabase
_supabase_client: Optional[Client] = None

def init_db() -> Client:
    """
    Inicializa la conexión a la base de datos y devuelve el cliente de Supabase.
    Asegura que el cliente se inicialice una sola vez (patrón Singleton).
    """
    global _supabase_client
    if _supabase_client is None:
        logger.info("Inicializando la conexión a la base de datos...")
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            error_msg = "Error: Las variables de entorno SUPABASE_URL o SUPABASE_SERVICE_KEY no están configuradas."
            logger.error(error_msg)
            raise ValueError(error_msg)
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            logger.info("Conexión a Supabase establecida correctamente.")
        except Exception as e:
            error_msg = f"Error al conectar con Supabase: {e}"
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
    return _supabase_client

# Función para probar la conexión
def test_connection():
    try:
        supabase_client = init_db()
        # Puedes realizar una operación simple para verificar la conexión, por ejemplo:
        # response = supabase_client.from_('your_table').select('*').limit(1).execute()
        # if response.data is not None:
        print("Conexión a Supabase verificada y activa.")
    except (ValueError, ConnectionError) as e:
        print(f"Fallo en la conexión a Supabase: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al probar la conexión: {e}")

  


