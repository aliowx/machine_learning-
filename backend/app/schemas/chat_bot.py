from pydantic import BaseModel, HttpUrl
from typing import Optional, Any, Dict
from datetime import datetime

class ChatbotBase(BaseModel):
    message: str
    web_service_url: Optional[str] = None
    
    
    
class ChatbotCreate(ChatbotBase):...


class ChatbotUpdate(ChatbotBase):
    message: Optional[str] = None
    web_service_url: Optional[HttpUrl] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None