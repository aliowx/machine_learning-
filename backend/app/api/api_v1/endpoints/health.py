import time 
from fastapi import APIRouter, Depends
from app.core.config import settings
from app.api.deps import health_user, get_redis
from app import schemas, crud
from app.utils import utils
from app.db import session



router = APIRouter()



@router.get("/ping", response_model=bool)
def ping(_=Depends(health_user))-> bool: 
    """
    Return 'True'
    """
    return True