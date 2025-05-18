from pydantic import BaseModel, field_validator, AnyUrl
from typing import Optional, Dict, Any
from datetime import datetime


class InputSchema(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None

class OutputSchema(BaseModel):
    name: str
    type: float
    description: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None


class MLModelBase(BaseModel):
    id: int = None
    model_name: str = None
    version: str = None
    model_file_path: str = None
    description: str = None
    
    @field_validator('Model')
    def validate_model(cls, v):
        if v and v.lower() not in ["scikit-learn", "tensorflow", "pytorch", "xgboost", "lightgbm"]:
            raise ValueError("Unsupported the Model")
        return  v

    
    @field_validator('Task')
    def validate_task(cls, v):
        if v and v.lower() not in ["classification", "regression", "clustering", "nlp", "other"]:
            raise ValueError("Unsupported task type")
        return v
    
class ModelVersionBase(BaseModel):
    id: int | None = None
    version_name: str | None = None
    model_file_path: str | None = None
    
    


class ModelVersionCreate(ModelVersionBase):...



class ModelVersionUpdate(ModelVersionBase):...


class ModelVersionInDBBase():...