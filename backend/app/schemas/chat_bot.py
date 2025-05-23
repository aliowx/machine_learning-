from pydantic import BaseModel, HttpUrl
from typing import Optional, Any, Dict
from datetime import datetime

class ChatbotBase(BaseModel):
    message: str
    
    
    
class ChatbotCreate(ChatbotBase):...


class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    user_id: Optional[str] = None

class ChatbotUpdate(ChatbotBase):
    message: Optional[str] = None
    web_service_url: Optional[HttpUrl] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None