from pydantic import BaseModel, HttpUrl
from typing import Optional, Any, Dict
from datetime import datetime

class Chatbot(BaseModel):
    message: str
    
    
    
class ChatbotCreate(Chatbot):...

class ChatbotResponse(Chatbot):
    id: int
    message: str
    conversation_id: int
    is_bot: bool
    created_at: datetime
    bot_response: str
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None


class ChatbotUpdate(Chatbot):
    message: Optional[str] = None
    web_service_url: Optional[HttpUrl] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None