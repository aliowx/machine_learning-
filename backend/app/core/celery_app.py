from celery import Celery, Task
from app.core.config import settings

BROKER_URL = str(settings.REDIS_URI)


celery_app = Celery(
    "worker", backend="rpc://", broker=BROKER_URL, include=["celery.worker"]
)

celery_app.conf.update(task_track_started=True, broker_connection_retry_on_startup=True)



class DatabaseTask(Task):...