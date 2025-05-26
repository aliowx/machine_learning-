from typing import Any 
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_ , select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.chat_bot import ChatHistory
from app.schemas.chat_bot import ChatbotCreate, ChatbotUpdate



class CRUDChatBot(CRUDBase[ChatHistory, ChatbotCreate, ChatbotUpdate]):
    async def create_chat_message(db: AsyncSession, chat: ChatbotCreate, bot_response: str )-> ChatHistory:
        try:
            chat_data = jsonable_encoder(chat)
            
            
            chat_data['bot_response'] = bot_response
            
            db_chat = ChatHistory(**chat_data)
            
            db.add(db_chat)
            
            await db.commit()
            await db.refresh(db_chat)
            
            return db_chat
        except Exception as e:
            await db.rollback()
            raise Exception(f"Error creating chat message: {str(e)}")
        
        
        