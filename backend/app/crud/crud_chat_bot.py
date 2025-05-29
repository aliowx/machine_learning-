from typing import Any 
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_ , select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.chat_bot import ChatHistory
from app.schemas.chat_bot import ChatbotCreate, ChatbotUpdate, Chatbot
from typing import Optional 
import exceptions as exc
from app.utils import MessageCodes
import logging


logger = logging.getLogger(__name__)

class CRUDChatBot(CRUDBase[ChatHistory, ChatbotCreate, ChatbotUpdate]):
    async def create_chat_message(self, db: AsyncSession, chat: ChatbotCreate, bot_response: str, user_id: Optional[int]=None )-> ChatHistory:
        try:
            if not chat.message.split():
                raise exc.AlreadyExistException(
                    detail='Message cannot be empty',
                    msg_code=MessageCodes.bad_request
                )
            if not bot_response.split():
                raise exc.AlreadyExistException(
                    detail='Bot response cannot empty',
                    msg_code=MessageCodes.bad_request
                )
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
        

    
    async def get_messages_by_conversation_id(
        self,
        db: AsyncSession,
        conversation_id: int,
        limit: int = 10,
        offset: int = 0,
    )-> list[Chatbot]:
        try:
            query = select(self.model).where(
                and_(
                    self.model.user_id == conversation_id,
                    self.model.is_deleted.is_(None)
                )
            )
            response = await db.execute(query)
            return response.scalar_one_or_none()
        
        except:
            pass
chat = CRUDChatBot(ChatHistory)