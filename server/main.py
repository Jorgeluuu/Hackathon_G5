from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.itinerary_routes import router as itinerary_router
from server.core.database import init_db
from server.services.resource_loader import ResourceLoader
import os
from server.dependencies import set_resource_data # Importar set_resource_data

app = FastAPI(
    title="El Planificador Mágico del Ratoncito Pérez",
    description="API para planificar itinerarios mágicos en Madrid.",
    version="0.0.1",
)

# Configuración de CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes por ahora, ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variable global para almacenar los recursos cargados
resource_data = {}

@app.on_event("startup")
async def startup_event():
    init_db()
    # Inicializar y cargar los recursos
    resources_path = os.path.join(os.path.dirname(__file__), "resources")
    loader = ResourceLoader(resources_path)
    loader.load_all_resources()
    # Almacenar los datos cargados en la variable global
    global resource_data
    resource_data["festividades"] = loader.get_festividades_data()
    resource_data["links"] = loader.get_links_data()
    resource_data["madrid_destino"] = loader.get_madrid_destino_data()
    resource_data["transporte"] = loader.get_transporte_data()
    
    # Pasar los recursos cargados a la función en dependencies.py
    set_resource_data(resource_data)
    
    print("Todos los recursos cargados y disponibles.")

# Nueva función para obtener los recursos como una dependencia <-- ELIMINAR ESTAS LÍNEAS
# def get_resource_data():
#     return resource_data

app.include_router(itinerary_router, prefix="/api/v1")