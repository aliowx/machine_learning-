from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas, utils
from app.api import deps
from app.api.api_v1 import services
from app.log import log
from app.utils import APIResponse, APIResponseType
from app.cache import cache, invalidate
from app.cache.util import ONE_DAY_IN_SECONDS
from typing import Annotated
from app import exceptions as exc


router = APIRouter()
namespace = "predict"

# @router.post('')
# async def M