from fastapi import APIRouter, Depends, HTTPException 
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


def get_bot_response(user_message: str)-> str:
    user_message = user_message.lower()
    if "Hi" in user_message:
        return "how can i help ypu my dear!?"
    elif "By" in user_message:
        return "good by  😊"
    else:
        return "Opss"


chat_history: list[dict] = []

@router.post('/bot')
async def chatbot_process_message(
    message: ChatbotBase,
   _: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
) :
    if not message.message:
            raise HTTPException(status_code=400, detail="")

    bot_response = get_bot_response(message.message)
    

    chat_history.append({"user": message.message, "bot": bot_response})
    
    return {"user_message": message.message, "bot_response": bot_response}