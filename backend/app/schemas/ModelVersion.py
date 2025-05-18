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




class ModelVersionBase(BaseModel):
    id: int | None = None
    version_name: str | None = None
    model_file_path: str | None = None
    
    


class ModelVersionCreate(ModelVersionBase):...



class ModelVersionUpdate(ModelVersionBase):...


class ModelVersionInDBBase():...