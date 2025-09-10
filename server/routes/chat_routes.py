from fastapi import APIRouter
from server.controllers.chat_controller import chat_controller
from server.schemas.chat_schema import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return chat_controller(request)
