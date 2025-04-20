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