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
    async def get_output_model(self, outputs: str, db: AsyncSession, model_id: int, version :str) -> Optional[dict]:
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
            query = select(ModelVersion).filter(
                ModelVersion.model_id == model_id,
                ModelVersion.version == version
            )
            result = await db.execute(query)
            model_version = result.scalars().first()

            if not model_version:
                logger.warning(f"No model version found for model_id={model_id}, version={version}")
                return None
            
            outputs = model_version.outputs
            if not outputs:
                logger.info(f"No outputs found for model_id={model_id}, version={version}")
                return None
            if isinstance(outputs, str):
                try:
                    output_data = json.loads(outputs)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON outputs for model_id={model_id}, version={version}: {str(e)}")
                    raise ValueError(f"Invalid JSON data in outputs: {str(e)}")
            
            else:
                output_data = outputs
                
            if not isinstance(output_data, dict):
                logger.error(f"Output data is not a dictionary for model_id={model_id}, version={version}")    
                raise ValueError('Output data must be a dictionary')


            return output_data        
        except Exception as e:
            logger.exception(f'Error retrieving output for model_id={model_id}, version={version}: {str(e)}')
            
            
            
    async def get_model_versions(self, db: AsyncSession,model_id: int, limit: int = 100) -> list[dict]:...        
        