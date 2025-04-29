from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1 import services
from app.log import  log
from app.utils import APIResponse, APIResponseType
from app.cache import cache, invalidate
from app.cache.util import ONE_DAY_IN_SECONDS
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



@router.put('/{user_id}')
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def update_user(
    user_id: int,
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user_from_cookie_or_basic)
    
)-> APIResponseType[schemas.User]:
    """
    Update User
    """
    
    
    response = await services.update_user(
        user_id=user_id,
        user_in=user_in,
        db=db,
        current_user=current_user
    )
    return APIResponse(response)