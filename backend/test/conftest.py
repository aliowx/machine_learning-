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




app.dependency_overrides[get_db_async] = override_get_db_async


@pytest.fixture(autouse=True)
def patch_async_session_maker(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(db_session, "async_session", async_session)


@pytest.fixture(scope="session")
def even_loop()-> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop 
    loop.close()
    

@pytest_asyncio.fixture(scope='session')
async def async_db()-> AsyncGenerator:
    async with async_session() as session:
        async with async_engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
        await init_db(db=session)
        yield session

    await async_engine.dispose()