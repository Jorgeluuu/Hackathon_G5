from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import generation_routes

app = FastAPI(
    title="Planificador Mágico API",
    description="API para agentes IA del Ratoncito Pérez",
    version="1.0.0"
)

# CORS para frontend (Dash)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8050", "http://127.0.0.1:8050"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(generation_routes.router, tags=["Generation"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Planificador Mágico API running"}
