from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    message: str
    sender: str = "mouse"
    timestamp: str
    created_with_fallback: bool = False
