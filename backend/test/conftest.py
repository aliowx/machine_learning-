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


