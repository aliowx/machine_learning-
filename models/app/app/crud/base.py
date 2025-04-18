from datetime import datetime
from typing import Any, Generator, Generic, Sequence, Type, TypeVar, Union, List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping, and_, exc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """

        self.model = model

    async def get(self, db: AsyncSession, id_: int | str) -> ModelType | None:
        query = select(self.model).where(
            and_(
                self.model.id == id_,
                self.model.is_deleted.is_(None) 
            )
        )
        response = await db.execute(query)
        return response.scalar_one_or_none()
        
