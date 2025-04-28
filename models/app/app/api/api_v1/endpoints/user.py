from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.app import crud, models, schemas
from app.app.api import deps
from app.app.api.api_v1 import services
from app.app.log import  log
from app.app.utils import APIResponse, APIResponseType



router = APIRouter()
namespace = 'user'


@router.get('/')
async def read_users(
    
)-> APIResponseType[list[schemas.User]]:...