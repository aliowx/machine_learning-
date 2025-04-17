from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class PredictionBase(BaseModel):
    prediction_result: str | None = None
    created_at: str | None = None
    
    
class PredictionCreate(PredictionBase):
    user_id: int
    model_version_id: int
    
    
    
    