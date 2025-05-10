from typing import Any
from fastapi import APIRouter, Depends, Request
from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.log import log
#____________________________________________________

router_with_log = APIRouter(route_class=log.LogRoute)
router = APIRouter()


