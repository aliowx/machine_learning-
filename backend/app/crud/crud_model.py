from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select
from app.schemas import MLModelCreate, MLModelBase
from app.crud.base import CRUDBase
from app.models import ModelVersion
import json
import logging 


logger = logging.getLogger(__name__)
class CRUDModel(CRUDBase[ModelVersion, MLModelCreate, MLModelBase]):
    async def get_output_model(self, outputs: str, db: AsyncSession) -> Optional[dict]:
        """
        Retrieve and parse the output of a specific model version from the database.
        
        Args:
            model_id (int): The ID of the machine learning model.
            version (str): The version of the model.
            db (AsyncSession): The async database session.
        
        Returns:
            Optional[dict]: The parsed JSON output of the model version, or None if not found or invalid.
        
        Raises:
            ValueError: If the output data is not valid JSON.
        """
        try:
            output_data = json.loads(outputs) if isinstance(output_data, str) else output_data
            
            if not isinstance(output_data, dict):
                raise ValueError("There is problem here about the json data")
            
            
        except:
            pass
        
        