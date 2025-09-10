from datetime import datetime
from server.schemas.chat_schema import ChatRequest, ChatResponse

def chat_with_mouse(chat_request: ChatRequest) -> ChatResponse:
    user_message = chat_request.message.lower()

    if "free" in user_message or "gratis" in user_message:
        answer = "✨ You can enjoy Parque del Retiro, Templo de Debod, and Plaza Mayor for free!"
    else:
        answer = "🧚 I’m the Magic Mouse! I’ll help you explore Madrid with tips and stories."

    return ChatResponse(
        message=answer,
        sender="mouse",
        timestamp=datetime.utcnow().isoformat(),
        created_with_fallback=False
    )
