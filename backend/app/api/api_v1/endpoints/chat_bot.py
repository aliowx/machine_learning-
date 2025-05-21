from fastapi import FastAPI ,Request, Response, APIRouter, Depends
from fastapi.openapi.models import OpenAPI
from app.core.config import settings
from app.log import log
from app.cache import invalidate, cache




router = APIRouter()

namespace = "ChatBot"



@router.get('/bot')
# @cache()
async def chat_bot():...
