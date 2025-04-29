from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app import exceptions as exc
from app.utils import  MessageCodes


async def read_user_by_id(
    user_id: int,
    current_user: models.User,
    db: AsyncSession
)-> schemas.User:
    
    user = await crud.user.get(db, id_=user_id)
    if not user:
        raise exc.NotFoundException(
            detail='User not found',
            msg_code=MessageCodes.not_found
        )
        
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise exc.ForbiddenException(
            detail="The user doesn't have enough privileges",
            msg_code=MessageCodes.bad_request,
        )
        
    return user



async def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: AsyncSession,
    current_user: models.User,
) -> schemas.User:
    if not current_user.is_superuser:
        if not current_user.id == user_id:
            raise exc.ForbiddenException(
                detail="You do not have permission to update other users",
                msg_code=MessageCodes.permission_error,
            )

    user = await crud.user.get(db, id_=user_id)
    if not user:
        raise exc.NotFoundException(
            detail="The user with this username does not exist",
            msg_code=MessageCodes.not_found,
        )
    user = await crud.user.update(
        db, db_obj=user, obj_in=user_in.model_dump(exclude_none=True)
    )
    return user
