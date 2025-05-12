from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas, utils
from app.api import deps
from app.api.api_v1 import services
from app.log import log
from app.utils import APIResponse, APIResponseType
from app.cache import cache, invalidate
from app.cache.util import ONE_DAY_IN_SECONDS
from typing import Annotated
from app import exceptions as exc

router = APIRouter()
namespace = "user"

@router.get("/")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def read_users(
    db: AsyncSession = Depends(deps.get_db_async),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
) -> APIResponseType[list[schemas.User]]:
    """
    Retrieve users.
    """
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return APIResponse(users)


@router.get("/{user_id}")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
    db: AsyncSession = Depends(deps.get_db_async),
) -> APIResponseType[schemas.User]:
    """
    Get a specific user by id.
    """
    response = await services.read_user_by_id(
        db=db, user_id=user_id, current_user=current_user
    )
    return APIResponse(response)


@router.put("/{user_id}")
@invalidate(namespace=namespace)
async def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user_from_cookie_or_basic),
) -> APIResponseType[schemas.User]:
    
    """
    Update a user.
    """
    
    response = await services.update_user(
        db=db, user_id=user_id, user_in=user_in, current_user=current_user
    )
    return APIResponse(response)


@router.get("/{user_id}")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def read_user_by_id(
    user_id: int,
    _: Annotated[
        bool,
        Depends(),
    ],
    current_user: models.User = Depends(deps.get_current_user_from_cookie_or_basic),
    db: AsyncSession = Depends(deps.get_db_async),
) -> APIResponseType[schemas.User]:
    """
    Get a specific user by id.
    """
    
    
    user = await crud.user.get(db=db, id=user_id)
    
    if not user:
        raise exc.ServiceFailure(
            msg_code=utils.MessageCodes.bad_request,
            detail=" User is not define! "
        )
        
        
        
        