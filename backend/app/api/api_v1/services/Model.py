from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.ModelVersion import MLModelCreate, MLModelBase
from app import crud 
from app.utils import MessageCodes
from typing import Any, Optional, List, Dict
import logging


logger = logging.getLogger(__name__)



class ModelService:
    def __init__(self)->None:
        pass
    
    
    
    
    async def get_model_output(
        self,
        db: AsyncSession,
        outputs: str,
        model_id: int,
        version: str,
    )-> Dict[str, Any]:
        
    pass