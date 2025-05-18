from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.schemas import UserCreate, UserBase, UserUpdate
from test.utils.utils import random_email ,random_lower_string




class TestUser:
    
    @pytest.mark.asyncio
    async def test_user_create(self, db: AsyncSession)-> UserCreate:...
