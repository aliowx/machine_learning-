from fastapi import FastAPI ,Request, HTTPException, APIRouter, Depends
from fastapi.openapi.models import OpenAPI
from app.core.config import settings
from app.log import log
from app.cache import invalidate, cache
import httpx
from typing import Optional
from app.schemas.chat_bot import ChatbotBase, ChatRequest
from app.core.config import settings
from app import exceptions as exc
from app import models
from app.api import deps


router = APIRouter()
namespace = "ChatBot"


@router.post('/bot')
# @cache()
async def chatbot_process_message(
    request: ChatRequest,
    api_key: str = Depends(deps.get_api_key), 
   _: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
)-> ChatbotBase :
    try:
        log.info(f"[{namespace}] Received message from user_id={request.user_id}: {request.message}")
        async with httpx.AsyncClient as client:
            response = await client.post(
                settings.CHATBOT_API_KEY,
                headers={"Authorization": f"Bearer {api_key}"},
                json={"message": request.message, "user_id": request.user_id},
                timeout=10.0
            )
            
    except:
        pass 