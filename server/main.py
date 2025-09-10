from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routes.itinerary_routes import router as itinerary_router
from server.routes.chat_routes import router as chat_router
from server.routes.recommendations_routes import router as recommendations_router

app = FastAPI(title="Magic Planner API - Ratoncito Pérez")

# CORS (ajústalo según tu front)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rutasss
app.include_router(itinerary_router, prefix="/api/v1/itinerary", tags=["Itinerary"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(recommendations_router, prefix="/api/v1/recommendations", tags=["Recommendations"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
