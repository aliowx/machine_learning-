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
    async def test_login_normal(self, client: AsyncClient):
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json=self.data
        )
        assert response.status_code == 200
        logger.info("Login test passed.")

    @pytest.mark.asyncio
    async def test_login_invalid(self, client: AsyncClient):
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json={"email": "invalied_email@in.valid", "password": "invalied_password"},
        )
        assert response.status_code == 404
        logger.info("Login invalid test passed.")
    @pytest.mark.asyncio
    async def test_auth_and_tokens(self, client: AsyncClient):
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json=self.data
        )
        assert response.status_code == 200
        logger.info("Auth and Tokens test passed.")
    
    @pytest.mark.asyncio
    async def call_service_with_access_and_refresh_tokens(self, client: AsyncClient):
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json=self.data
        )
        cookies = dict(response.cookies.items())
        
        response = await client.get(f'{settings.API_V1_STR}/auth/me', cookies=cookies)
        
        assert response.status_code == 404 
        logger.info("Call service access and tokens refresh test passed.")
        
    @pytest.mark.asyncio   
    async def test_login(self, client: AsyncClient):

        # normal login
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login", json=self.data
        )
        assert response.status_code == 200
        assert response.cookies.get("Access-Token") is not None
        assert response.cookies.get("Refresh-Token") is not None

        # invalid login
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json={"email": "invalied_email@in.valid", "password": "invalied_password"},
        )
        assert response.status_code == 200 