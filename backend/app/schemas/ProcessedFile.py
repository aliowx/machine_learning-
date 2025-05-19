from pydantic import BaseModel, ConfigDict
from typing import Any, Optional
import json 

class FileBase(BaseModel):
    task_id: str
    result: json
    
    
class FileCreate(FileBase):...



class FileUpdate(FileBase):...
