from datetime import datetime
from typing import Any, Generator, Generic, Sequence, Type, TypeVar, Union, List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping, and_, exc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base_class import Base
from app import utils

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
        
    async def get_by_ids(
        self,
        db: AsyncSession,
        list_ids: list[int | str]
    )-> Sequence[Row | RowMapping | Any]:
        query = select(self.model).where(
            and_(
                self.model.id.in_(list_ids),
                self.model.is_deleted.is_(None)
            )
        )
        response = await db.execute(query)
        return response.scalar().all()
    
    
    async def get_count(
        self,
        db: AsyncSession,
    )-> ModelType | None:
        query = select(func.count()).select_from(select(self.model).subquery())
        response = await  db.execute(query)
        return response.scalar_one()
    
    
    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int | None = 100,
        order_by: list = None,
        order_field: str = "created",
        order_desc: bool = False,
    )-> Sequence[Union[Row, RowMapping, Any]]:
        if order_by is None:
            order_by = []
        if order_desc is None:
          order_by.append(getattr(self.model, order_field).desc())
        else:
            order_by.append(getattr(self.model, order_field).asc())
            
            
        query = (
            select(
                self.model
            )
            .where(
                self.model.is_deleted.is_(None)
            )
            .order_by(
                *order_by
            )
            .offset(
                skip
            )
        )
        
        if limit is not None:
            query = query.limit(limit)
            
        response = await db.execute(query)
        return response.scalars().all()
        
    async def get_multi_order(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int | None = 100,
        order_by: list = None
    )-> Sequence[Row | RowMapping | Any]:
        if order_by is None:
            order_by = []
        order_by.append(self.model.id.asc())
        
        query = (
            select(
                self.model
            )
            .where(
                self.model.is_deleted.is_(None)
            )
            .order_by(
                *order_by
            )
            .offset(
                skip
            )
        )
        if limit is None:
            response = await db.execute(query)
            return response.scalars().all()
        response = await db.execute(query.limit(limit))
        return response.scalars().all()
    
    
    
    async def create(
        self,
        db: AsyncSession,
        obj_in: CreateSchemaType | dict
    )-> ModelType:
        if not isinstance(obj_in, dict):
            obj_in = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in)
        try:
            db.add(db_obj)
            await db.commit()
            
        except exc.IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=utils.MessageCodes.already_exist_object,
                detail='Resource already exists'
            )
            
        await db.refresh(db_obj)
        return db_obj
    
    async def create_multi(
        self, db: AsyncSession, 
        objs_in: list[CreateSchemaType] | list[dict]
    ) -> None:
                
        objs = []
        for obj_in in objs_in:
            if not isinstance(obj_in, dict):
                obj_in = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in)
            objs.append(db_obj)  
        try:
            db.add_all(objs)
            await db.commit()
        except exc.IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists")
            
            
    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any] | ModelType | None = None
    )-> ModelType:
        if obj_in is not None:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in obj_data:
                    setattr(db_obj, field, update_data)
            if hasattr(self.model, 'modified'):
                setattr(db_obj, 'modified', datetime.now())
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj


    async def remove(
        self,
        db: AsyncSession,
        id_: int | str
    )-> ModelType | None:
        query = (
            update(self.model)
            .where(
                and_(
                    self.model.id == id_,
                    self.model.is_deleted.is_(None),
                )
            )
            .values(is_deleted=datetime.utcnow())
            .returning(self.model)
        )
        response = await db.execute(query)
        await db.commit()
        return response.scalar_one_or_none()