import time
from redis.asyncio import client
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app import exceptions as exc
from app import schemas, utils
from app.core.config import REFRESH_TOKEN_BLOCKLIST_KEY, ACCESS_TOKEN_BLOCKLIST_KEY
from app.core.security import JWTHandler
import logging

logger = logging.getLogger(__name__)


async def register(db: AsyncSession, user_in: schemas.UserCreate) -> schemas.User:
    logger.info(f"Attempting to register user: {user_in.email}")
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    print(user)
    if user:
        logger.warning(f"User already exists: {user_in.email}")
        raise exc.AlreadyExistException(
            detail="The user with this username already exists",
            msg_code=utils.MessageCodes.bad_request,
        )
    user = await crud.user.create(db=db, obj_in=user_in)
    if not user:
        print("there isn't any user ")
    return user


async def login(db: AsyncSession, user_in: schemas.LoginUser) -> schemas.Token:
    user = await crud.user.authenticate(
        db=db, email=user_in.email, password=user_in.password
    )
    if not user:
        raise exc.NotFoundException(
            detail="Incorrect email or password",
            msg_code=utils.MessageCodes.incorrect_email_or_password,
        )

    refresh_token = JWTHandler.encode_refresh_token(
        payload={"sub": "refresh", "id": str(user.id)}
    )
    access_token = JWTHandler.encode(payload={"sub": "access", "id": str(user.id)})

    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def logout(refresh_token: str, access_token: str, cache: client.Redis):
    if not cache:
        raise exc.InternalErrorException(
            detail="Redis connection is not initialized",
            msg_code=utils.MessageCodes.internal_error,
        )

    try:
        if refresh_token:
            refresh_token_key = REFRESH_TOKEN_BLOCKLIST_KEY.format(token=refresh_token)
            await cache.set(
                refresh_token_key,
                time.time(),
                ex=JWTHandler.token_expiration(refresh_token),
            )
    except exc.UnauthorizedException:
        pass

    try:
        if access_token:
            access_token_key = ACCESS_TOKEN_BLOCKLIST_KEY.format(token=access_token)
            await cache.set(
                access_token_key,
                time.time(),
                ex=JWTHandler.token_expiration(access_token),
            )
    except exc.UnauthorizedException:
        pass
