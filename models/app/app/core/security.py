from datetime import datetime, timedelta
from hashlib import sha256
from typing import Any
import jwt 
import bcrypt

from fastapi.security import HTTPBasic
from app import exceptions as exc

from app.core.config import settings
from app.utils import MessageCodes


