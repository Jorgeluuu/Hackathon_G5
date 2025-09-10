from fastapi import HTTPException
from server.schemas.chat_schema import ChatRequest, ChatResponse
from server.services.chat_service import chat_with_mouse

def chat_controller(request: ChatRequest) -> ChatResponse:
    try:
        return chat_with_mouse(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
