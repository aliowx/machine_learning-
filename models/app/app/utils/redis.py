import redis.asyncio as redis

from app.app.core.config import settings


redis_url = str(settings.REDIS_URI)

redis_pool = redis.ConnectionPool.from_url(
    redis_url,
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=redis_pool)