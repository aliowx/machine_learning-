from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select
from app.schemas import MLModelCreate, MLModelBase
from app.crud.base import CRUDBase
from app.models import ModelVersion


class CRUDModel(CRUDBase[ModelVersion, MLModelCreate, MLModelBase]):
    async def get_output_model(self, outputs: str, db: AsyncSession):...