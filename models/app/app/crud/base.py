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
