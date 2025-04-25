from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1 import services
from app.log import  log
from app.utils import APIResponse, APIResponseType



router = APIRouter()
namespace = 'user'


@router.get('/')
async def read_users(
    
)-> APIResponseType[list[schemas.User]]:...