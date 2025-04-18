from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class PredictionBase(BaseModel):
    prediction_result: str | None = None
    created_at: str | None = None
    
    
class PredictionCreate(PredictionBase):
    user_id: int
    model_version_id: int
    


class PredictionInDBBase(PredictionBase):
    id: int | None = None
    model_config = ConfigDict(from_attributes=True)
    

class Prediction(PredictionInDBBase):...




class PredictionIn(BaseModel):
    user_id: int
    model_version_id: int
    
    
    