import pytest 
from httpx import AsyncClient, BasicAuth
from app.core.config import settings
import logging 
from app import schemas

logger = logging.getLogger(__name__)


class TestHealth:
    
    @pytest.mark.asyncio
    async def test_ping(self, client: AsyncClient):
        response = await client.get(
          f"{settings.API_V1_STR}/health/ping",
          auth=BasicAuth(
            username=settings.HEALTH_USERNAME,password=settings.HEALTH_PASSWORD 
          ),
        )
        
        assert response.status_code == 200
        logger.info("This test pass!")