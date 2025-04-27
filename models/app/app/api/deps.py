import logging 
import secrets
from typing import AsyncGenerator
from fastapi.security import HTTPBasicCredentials
import redis.asyncio as redis
from fastapi import Depends, Request, Response
from redis.asyncio import client
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models, utils
from app import exceptions as exc
from app.utils import redis_client
 
from app.core.config import(
    settings,
    ACCESS_TOKEN_BLOCKLIST_KEY,
    REFRESH_TOKEN_BLOCKLIST_KEY
)
from app.core.security import JWTHandler, basic_security
from app.db.session import async_session

logger = logging.getLogger(__name__)   

async def get_db_async() -> AsyncGenerator:
    # get database///

    async with async_session() as session:
        yield session 
        
        
async def get_redis() -> client.Redis:
    try:
        if await redis_client.ping():
            return redis_client
        raise redis.RedisError('ping Error')
    except Exception as e:
        logger.error(f"Redis connection failed\n{e}")
        raise e 
    
    
    
async def get_user_id_from_cookie(
    request: Request,
    response: Response,
    cache: client.Redis = Depends(get_redis)
):
    try:
        access_token = request.cookies.get('Access-Token')
        
        if not access_token:
            
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.access_token_not_found
            )  
            
            
        token = JWTHandler.decode(access_token)
        if await cache.get(ACCESS_TOKEN_BLOCKLIST_KEY.format(token=access_token)):
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.expired_token
            )
        
        user_id = token.get('id')
        if token.get('sub') != 'access' or not user_id:
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.invalid_token
            )
            
    except:
        refresh_token = request.cookies.get('Refresh-Token')
        if not refresh_token:
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.refresh_token_not_found
            )
            
        refresh_token_data = JWTHandler.decode(refresh_token)
        
        
        if (
            await cache.get(REFRESH_TOKEN_BLOCKLIST_KEY.format(token=refresh_token))
            or refresh_token_data.get("sub") != "refresh"            
        ):
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.invalid_token
            )
            
            
            
        user_id = refresh_token_data.get('id')
        
        token = JWTHandler.encode(payload={"sub": "access", "id": user_id})
        
        
        response.set_cookie(
            key="Access-Token",
            value=token,
            secure=True,
            httponly=True,
            samesite="strict" if not settings.DEBUG else "none",
            expires=JWTHandler.token_expiration(token),
        )
        
    request.state.user_id = user_id

    return int(user_id)



async def get_current_user_from_cookie(
    db: AsyncSession = Depends(get_db_async),
    current_user_id: int = Depends(get_user_id_from_cookie)
) -> schemas.User:
    
    current_user = await crud.user.get(db=db, id_=current_user_id)
    
    
    if not current_user:
        raise exc.ForbiddenException(msg_code=utils.MessageCodes.invalid_token)
    
    if not crud.user.is_active(current_user):
        raise exc.ForbiddenException(msg_code=utils.MessageCodes.inactive_user)
    
    return current_user




def get_current_superuser_from_cookie(
    current_user: models.User = Depends(get_current_user_from_cookie)
) -> models.User:
    
    if not crud.user.is_superuser(current_user):
        raise exc.ForbiddenException(
            detail="Permission Error",
            msg_code=utils.MessageCodes.permission_error,
        )
    return current_user




def _get_basic_credentials(
    credentials: HTTPBasicCredentials = Depends(basic_security)
)-> tuple[str,str]:
    if not credentials or not credentials.username or not credentials.password:
        raise exc.UnauthorizedException(
            msg_code=utils.MessageCodes.not_authorized,
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials



def health_user(
    credentials: HTTPBasicCredentials = Depends(_get_basic_credentials),
) -> str:

    if not (
        secrets.compare_digest(
            credentials.username.encode("utf8"), settings.HEALTH_USERNAME.encode("utf8")
        )
        and secrets.compare_digest(
            credentials.password.encode("utf8"), settings.HEALTH_PASSWORD.encode("utf8")
        )
    ):
        raise exc.UnauthorizedException(
            msg_code=utils.MessageCodes.incorrect_email_or_password,
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username



