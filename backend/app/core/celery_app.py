from celery import Celery, Task
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings

celery_app = Celery(
    "worker",
    backend="rpc://",
    broker=str(settings.REDIS_URI),
    include=["celery.worker"],
)


ScopedSession = None

from celery.signals import worker_init


@worker_init.connect
def bootstrap(*args, **kwargs):
    global ScopedSession
    engine = create_engine(
        str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    ScopedSession = scoped_session(SessionLocal)


class DatabaseTask(Task):
    abstract = True

    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.remove()

    @property
    def session(self):
        if self._session is None:
            self._session = ScopedSession

        return self._session


celery_app.conf.update(
    task_track_started=True, broker_connection_retry_on_startup=True
)
