from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat_bot import ChatbotCreate
import aiohttp
from typing import Optional

class ChatbotService:
    def __init__(self)->None:
        pass
    
    
    async def process_message(self, db: AsyncSession, chat: ChatbotCreate) -> str:
        
        pass 