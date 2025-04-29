from pydantic import BaseModel, CockroachDsn
from typing import Optional


class ModelVersionBase(BaseModel):
    id: int | None = None
    version_name: str | None = None
    model_file_path: str | None = None
    
    


class ModelVersionCreate(ModelVersionBase):...



class ModelVersionUpdate(ModelVersionBase):...


class ModelVersionInDBBase():...