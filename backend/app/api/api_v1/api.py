from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, user, health, utils, upload_csv, chat_bot

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(utils.router, prefix='/utils', tags=["utils"])
api_router.include_router(upload_csv.router, prefix='/csv', tags=["csv"])
api_router.include_router(chat_bot.router, prefix='/chat_bot', tags=["Chatbot"])