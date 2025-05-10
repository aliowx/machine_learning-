from typing import Any
from fastapi import APIRouter, Depends, Request
from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.log import log
#____________________________________________________

router_with_log = APIRouter(route_class=log.LogRoute)
router = APIRouter()


@router_with_log.post("test-db-log", response_model=schemas.Msg, status_code=200)
def test_db_log(
    request: Request,
    tracker_id: str,
    _: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
) -> Any:
    """
    This is an example of using log route handler.
    """
    request.state.tracker_id = tracker_id

    return schemas.Msg(msg="your request logged in my db!")

@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(
        deps.get_current_superuser_from_cookie_or_basic
    ),
) -> Any:
    """
    Test Celery worker.
    """
    task = celery_app.send_task("app.celery.worker.test_celery", args=[msg.msg])
    return {
        "msg": f"{msg.msg} - {task.id}",
    }
