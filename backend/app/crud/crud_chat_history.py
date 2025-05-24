from typing import Any 
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_ , select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.chat_bot import ChatHistory
from app.schemas.chat_bot import ChatbotCreate, ChatbotUpdate



class CRUDChatBot(CRUDBase[ChatHistory, ChatbotCreate, ChatbotUpdate]):
    async def create_chat_message(db: AsyncSession, chat: ChatbotCreate, bot_response:str ):pass