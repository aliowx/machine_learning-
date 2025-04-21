from datetime import datetime, timedelta
from hashlib import sha256
from typing import Any
import jwt 
import bcrypt

from fastapi.security import HTTPBasic
from app import exceptions as exc

from app.core.config import settings
from app.utils import MessageCodes


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
        expire=...

