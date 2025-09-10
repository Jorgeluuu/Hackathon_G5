from fastapi import HTTPException
import time
from models.itinerary_model import SimpleGenerationRequest, PromptRequest, ImagenRequest
from services.ai_service import generate_content
from services.image_service import generar_imagen
from services.utils import UID_REGEX, get_user_bio
from services.tracking_service import save_traceability
from services.nlp_service import generate_summary

class GenerationController:

    @staticmethod
    def generate_text(req: SimpleGenerationRequest):
        """Generar texto simple con agentes IA"""
        if not req.topic.strip():
            raise HTTPException(status_code=400, detail="Topic is required")
        if not req.platform:
            raise HTTPException(status_code=400, detail="Platform is required")

        user_bio = get_user_bio(req.uid)
        topic_with_context = f"Contexto del usuario: {user_bio}\n\nTema: {req.topic}" if user_bio else req.topic

        start_time = time.time()
        content = generate_content(
            platform=req.platform,
            topic=topic_with_context,
            language=req.language,
            provider="groq"
        )
        exec_time = time.time() - start_time

        save_traceability(req.uid, req.topic, req.language, content, exec_time)

        return {"content": content}

    @staticmethod
    def generate_news(req: PromptRequest):
        """Generar resumen NLP para noticias"""
        start_time = time.time()
        user_bio = get_user_bio(req.uid)

        context = req.prompt
        if user_bio:
            context = f"Contexto del usuario: {user_bio}\n\n{req.prompt}"

        resumen = generate_summary(context, language=req.language)
        exec_time = round(time.time() - start_time, 2)

        save_traceability(req.uid, req.prompt, req.language, resumen, exec_time)

        return {"response": resumen}

    @staticmethod
    def generate_image(req: ImagenRequest):
        """Generar imagen con fallback"""
        return generar_imagen(req)
