from pydantic import BaseModel, HttpUrl
from typing import Optional, Any, Dict
from datetime import datetime

class Chatbot(BaseModel):
    message: str

class ChatbotCreate(Chatbot):
    conversation_id: int
    is_bot: bool = False 

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
    conversation_id: int
    user_id: Optional[int] = None

class ChatbotUpdate(Chatbot):
    message: Optional[str] = None
    conversation_id: Optional[int] = None
    is_bot: Optional[bool] = None
    bot_response: Optional[str] = None