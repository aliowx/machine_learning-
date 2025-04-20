from typing import Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.db.base_class import  Base
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password




class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(
        self,
        db: AsyncSession,
        email: str
    )-> User | None:
        query = select(self.model).where(
            and_(
                self.model.email == email,
                self.model.is_deleted.is_(None),
            )
        )
        response = await db.execute(query)
        return response.scalar_one_or_none()
    
    async def create(
        self,
        db: AsyncSession,
        obj_in: UserCreate | dict  
    )-> Base | None:
        if isinstance(obj_in, dict):
            password = obj_in['password']
        else:
            password = obj_in.password
            
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['hashed_password'] = get_password_hash(password)
        del obj_in_data['password']
        
        obj_in_data = {k: v for k, v in obj_in_data.items() if v is not None}

        return await super().create(db, obj_in=obj_in_data)
    
    
    async def update(
        self,
        db: AsyncSession,
        db_obj: User,
        obj_in: UserUpdate | dict[str, Any] | None = None
    )-> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if 'password' in update_data and update_data['password']:
            hashed_password = get_password_hash(update_data['password'])
            del  update_data['password']
            update_data['hashed_password'] = hashed_password
            return await super().update(db=db, obj_in=obj_in,obj_in=update_data)