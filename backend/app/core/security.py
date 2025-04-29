from datetime import datetime, timedelta
from hashlib import sha256
from typing import Any
import jwt 
import bcrypt

from fastapi.security import HTTPBasic
import jwt.exceptions
from app.app import exceptions as exc

from app.app.core.config import settings
from app.app.utils import MessageCodes


basic_security = HTTPBasic(auto_error=False)

def verify_password(plain_password:str, hashed_password:str)-> bool:
    return hashed_password == sha256(plain_password.encode()).hexdigest()



def get_password_hash(password: str)-> str:
    return sha256(password.encode()).hexdigest()


class JWTHandler:
    secret_key = settings.SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    @staticmethod 
    def encode(payload: dict[str, Any])-> str:
        expire = datetime.utcnow() + timedelta(minutes = JWTHandler.access_token_expire)
        payload.update({'exp': expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm = JWTHandler.algorithm
        )
        
    @staticmethod
    def encode_refresh_token(payload: dict[str, Any])-> str:
        expire = datetime.utcnow() + timedelta(minutes = JWTHandler.refresh_token_expire)
        payload.update({"exp": expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm = JWTHandler.algorithm
        )

    @staticmethod
    def decode(token: str)-> dict:
        try:
            result: dict = jwt.decode(
                token, JWTHandler.secret_key, algorithms = [JWTHandler.algorithm]
            )
            return result
        except jwt.ExpiredSignatureError:
            raise exc.UnauthorizedException(
                detail = "Token expired",
                msg_code = MessageCodes.expired_token,
            )
        except jwt.InvalidTokenError:
            raise exc.UnauthorizedException(
                detail = "Invalid token",
                msg_code = MessageCodes.invalid_token,
            )
        
        
        
    @staticmethod
    def decode_expired(token: str)-> dict:
        try:
            return jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms = [JWTHandler.algorithm],
                options = {"verify_exp": False},
            )
        except jwt.InvalidTokenError:
            raise exc.UnauthorizedException(
                detail = "Invalid token",
                msg_code = MessageCodes.invalid_token,
            )
    
    @staticmethod
    def token_expiration(token: str)-> datetime | None:
        try:
            decoded_token = jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms = [JWTHandler.algorithm],
                options={"verify_exp": True},                
            )
            exp = int(decoded_token.get('exp'))
            if not exp:
                raise exc.UnauthorizedException(
                    detail = 'Invalid token exp',
                    msg_code = MessageCodes.invalid_token
                )
            return exp 
        except jwt.ExpiredSignatureError:
            raise exc.UnauthorizedException(
                detail = 'Token expire',
                msg_code = MessageCodes.expired_token
            )
        except jwt.InvalidTokenError:
            raise exc.UnauthorizedException(
                detail = 'Invalid token',
                msg_code = MessageCodes.invalid_token
            )