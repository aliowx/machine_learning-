import time 
from fastapi import APIRouter, Depends
from app.core.config import settings
from app.api.deps import health_user, get_redis
from app import schemas, crud
from app.utils import utils
from app.db import session



router = APIRouter()



@router.get("/ping", response_model=bool)
def ping(_=Depends(health_user))-> bool: 
    """
    Return 'True'
    """
    return True




@router.get("/check", response_model=schemas.HealthCheck)
async def deep_check(_=Depends(health_user)) -> schemas.HealthCheck:
    """
    check internal and external services
    """

    health = schemas.HealthCheck()

    health.app_version = settings.APP_VERSION
    health.commit_id = settings.COMMIT_ID

    health.uptime, health.human_readable_uptime = utils.get_linux_uptime()

    # Redis and Cache
    start = time.time()
    try:
        await get_redis()
        health.services.redis.ok = True
        health.services.redis.msg = "Redis is ok"
        health.services.redis.time = time.time() - start

    except Exception as e:
        health.ok = False
        health.services.redis.ok = False
        health.services.redis.msg = f"ERROR: {str(type(e))}, {str(e)}"
        health.services.redis.time = time.time() - start

    # Postgres
    start = time.time()
    try:
        async with session.async_session() as db:
            user = await crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)

        if user:
            health.services.postgres.ok = True
            health.services.postgres.msg = f"first user found: {user.email}"
            health.services.postgres.time = time.time() - start

        else:
            health.ok = False
            health.services.postgres.ok = False
            health.services.postgres.msg = "first user not found."
            health.services.postgres.time = time.time() - start

    except Exception as e:
        health.ok = False
        health.services.postgres.ok = False
        health.services.postgres.msg = f"ERROR: {str(type(e))}, {str(e)}"
        health.services.postgres.time = time.time() - start

    return health
