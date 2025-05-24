from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select
from app.schemas import MLModelCreate, MLModelBase
from app.crud.base import CRUDBase
from app.models import ModelVersion
import json

class CRUDModel(CRUDBase[ModelVersion, MLModelCreate, MLModelBase]):
    async def get_output_model(self, outputs: str, db: AsyncSession) -> Optional[dict]:
        try:
            output_data = json.loads(outputs) if isinstance(output_data, str) else output_data
            
            if not isinstance(output_data, dict):
                raise ValueError("There is problem here about the json data")
            
            
        except:
            pass