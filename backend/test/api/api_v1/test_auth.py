import pytest
from httpx import AsyncClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class TestAuth:
    @property
    def data(self):
        return {"email": "test@gmail.com", "password": "password"}

    @pytest.mark.asyncio
    async def test_register(self, client: AsyncClient, superuser_tokens:dict):
        response = await client.post(
            f"{settings.API_V1_STR}/auth/register",
            json=self.data,
            cookies=superuser_tokens
        )
        assert response.status_code == 200
        logger.info("Register test passed.")

    @pytest.mark.asyncio
    async def test_register_duplicate(self, client: AsyncClient, superuser_tokens:dict):
        response = await client.post(
            f"{settings.API_V1_STR}/auth/register",
            json=self.data,
            cookies=superuser_tokens
        )
        assert response.status_code == 409
        logger.info("Duplicate register test passed.")

    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient):
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json=self.data
        )
        assert response.status_code == 200
        logger.info("Login test passed.")

    @pytest.mark.asyncio
    async def test_me(self, client: AsyncClient, superuser_tokens:dict):
        response = await client.get(
            f"{settings.API_V1_STR}/me",
            cookies=superuser_tokens
        )
        
        assert response.status_code == 200