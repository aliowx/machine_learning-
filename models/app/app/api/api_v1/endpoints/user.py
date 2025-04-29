from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.app import crud, models, schemas
from app.app.api import deps
from app.app.api.api_v1 import services
from app.app.log import  log
from app.app.utils import APIResponse, APIResponseType
from app.app.cache import cache, invalidate
from app.app.cache.util import ONE_DAY_IN_SECONDS
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()
namespace = 'user'


@router.get('/')
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def read_users(
    db: AsyncSession = Depends(deps.get_db_async),
    skip: int = 0,
    limit: int = 100,
    _ : models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
)-> APIResponseType[list[schemas.User]]:
    
    users = await crud.user.get_multi(db=db, skip=skip, limit=limit)
    return APIResponse(users)