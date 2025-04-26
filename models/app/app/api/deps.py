import logging 
import secrets
from typing import AsyncGenerator
from fastapi.security import HTTPAuthorizationCredentials
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
            
    except :...