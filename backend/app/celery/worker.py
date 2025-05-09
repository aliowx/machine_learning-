import logging 
import math 
import random
from datetime import datetime, timedelta, UTC
from app.core.celery_app import DatabaseTask, celery_app



namespace = "job worker"

logger = logging.getLogger(__name__)


@celery_app.task(
    base=DatabaseTask,
    bind=True,
    acks_late=True,
    max_retries=4,
    soft_time_limit=240,
    time_limit=360,
    name="add_events",
)
def test(word: str)->str:
    return f"task celery app {word}"