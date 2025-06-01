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
        model_id: int,
        version: str,
    ) -> Dict[str, Any]:
        """
        Retrieve and parse output data for a specific model version.
        """
        try:
            if not model_id or not version:
                return {
                    "code": MessageCodes.bad_request,
                    "message": "Both model_id and version are required",
                    "data": None
                }

            result = await crud.model.get_output_model(
                db=db,
                model_id=model_id,
                version=version
            )

            if result is None:
                return {
                    "code": MessageCodes.bad_request,
                    "message": "No output found for the specified model version",
                    "data": None
                }

            return {
                "code": MessageCodes.successful_operation,
                "message": "Model output retrieved successfully",
                "data": result
            }

        except ValueError as ve:
            logger.warning(f"[ModelService] Invalid output data: {ve}")
            return {
                "code": MessageCodes.bad_request,
                "message": str(ve),
                "data": None
            }

        except Exception as e:
            logger.exception(f"[ModelService] Unexpected error: {e}")
            return {
                "code": MessageCodes.bad_request,
                "message": "An unexpected error occurred",
                "data": None
            }