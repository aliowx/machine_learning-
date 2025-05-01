from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, user, health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(health.router, prefix="/health", tags=["health"])