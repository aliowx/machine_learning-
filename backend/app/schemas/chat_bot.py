from pydantic import BaseModel, HttpUrl
from typing import Optional, Any, Dict
from datetime import datetime

class Chatbot(BaseModel):
    message: str
    
    
    
class ChatbotCreate(Chatbot):...

class ChatbotResponse(Chatbot):...

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None


class ChatbotUpdate(Chatbot):
    message: Optional[str] = None
    web_service_url: Optional[HttpUrl] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None