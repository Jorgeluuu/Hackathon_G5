import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Obtener las variables de entorno para las claves
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

# Crear el cliente de Supabase
# Se usa un if para asegurar que las variables no están vacías
if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
else:
    supabase = None
    print("Error: Las variables de entorno de Supabase no están configuradas.")

#Función para probar la conexión
def test_connection():
    if supabase:
        print("Conexión a Supabase establecida correctamente.")
    else:
        print("Fallo en la conexión a Supabase.")