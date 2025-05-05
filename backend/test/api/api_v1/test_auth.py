import pytest
from httpx import AsyncClient, BasicAuth
from app.core.config import settings
from app.schemas.user import UserCreate



@pytest.mark.asyncio
class TestAuth:
    email: str = "test@gmail.com"
    password: str = "password"
    
    
    @property
    def data(self):
        return {"email": TestAuth.email, "password": TestAuth.password}
    
    
    
    async def test_register(self, client: AsyncClient, superuser_tokens: dict):
        
        response = await client.post(
            f"{settings.API_V1_STR}/auth/register",
            json=self.data,
            cookies=superuser_tokens
        )
        assert response.status_code == 200
        
    async def test_register_duplicate(self, client: AsyncClient, superuser_tokens: dict):
        
        response = await client.post(
            f"{settings.API_V1_STR}/auth/register",
            json=self.data,
            cookies=superuser_tokens,
        )
        assert response.status_code == 409



