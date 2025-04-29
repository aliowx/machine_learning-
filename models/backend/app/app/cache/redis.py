import os 
import redis.asyncio as redis
from typing import Tuple
from redis.asyncio import client
from app.app.cache.enums import RedisStatus




async def redis_connect(host_url: str) -> Tuple[RedisStatus, client.Redis]:
    return ( await
        _connect(host_url)
    )


async def _connect(host_url: str) -> Tuple[RedisStatus, client.Redis]:
    try:
        redis_client = await redis.from_url(host_url)
        if await redis_client.ping():
            return RedisStatus.CONNECTED, redis_client
        return RedisStatus.CONNECTED, None
    except redis.AuthenticationError:
        return (RedisStatus.AUTH_ERROR, None)
    except redis.ConnectionError:
        return (RedisStatus.CONN_ERROR, None)


