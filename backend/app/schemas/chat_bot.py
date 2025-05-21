from pydantic import BaseModel
from typing import Optional, Any


class ChatbotBase(BaseModel):
    message: str
    web_service_url: Optional[str] = None
    
    
    
class ChatbotCreate(ChatbotBase):...




