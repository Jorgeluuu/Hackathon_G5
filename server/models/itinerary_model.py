from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str
    language: str
    coin_name: Optional[str] = None
    uid: Optional[str] = None

class ImagenRequest(BaseModel):
    tema: str
    audiencia: str
    estilo: str
    colores: str
    detalles: str = ""

class SimpleGenerationRequest(BaseModel):
    platform: str
    topic: str
    language: str
    uid: Optional[str] = None
