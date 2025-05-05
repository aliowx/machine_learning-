import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import  TestClient
from httpx import AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.api.deps import get_db_async
from app.main import app, settings
from app.db import Base
from app.crud import crud_user
from app.core.security import JWTHandler
from app.db.init_db import init_db
from app.db import session as db_session

ASYNC_SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///./test.db"


async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_db_async() -> AsyncGenerator:
    async with async_session() as db:
        yield db
        await db.commit()


