import pytest
from httpx import AsyncClient, BasicAuth
from app.core.config import settings




@pytest.mark.asyncio
class TestAuth:
    email: str = "test@gmail.com"
    password: str = "password"
    
    
    @property
    def data(self):
        return {"email": TestAuth.email, "password": TestAuth.password}
    
    
    
    # async def 