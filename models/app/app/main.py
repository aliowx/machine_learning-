from contextlib import asynccontextmanager
import logging, sys, os
from fastapi import FastAPI, Request, Response
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from app.app.core.middleware.get_accept_language_middleware import GetAcceptLanguageMiddleware
from app.app.api.api_v1.api import api_router
from app.app.core.config import settings
from app.app.core.middleware import TimeLoggerMiddleware
from app.app.exceptions import exception_handlers
from app.app.models import User
from app.app.cache import Cache

# تعریف مسیر پوشه build فرانت‌اند
current_dir = os.path.dirname(__file__)
frontend_build_dir = os.path.join(current_dir, "../../frontend/build") 
static_dir = os.path.join(frontend_build_dir, "static")  

def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(levelname)s:%(asctime)s %(name)s:%(funcName)s:%(lineno)s %(message)s"
        )
    )
    logger.addHandler(handler)

init_logger()

def make_middleware() -> list[Middleware]:
    middleware = []
    if settings.DEBUG:
        middleware.append(Middleware(TimeLoggerMiddleware))
    return middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_cache = Cache()
    url = str(settings.REDIS_URI)
    await redis_cache.init(
        host_url=url,
        prefix="api-cache",
        response_header="X-API-Cache",
        ignore_arg_types=[Request, Response, Session, AsyncSession, User],
    )
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    exception_handlers=exception_handlers,
    middleware=make_middleware(),
)

if settings.SUB_PATH:
    app.mount(f"{settings.SUB_PATH}", app)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):

    file_path = os.path.join(frontend_build_dir, full_path)

    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return FileResponse(file_path)

    return FileResponse(os.path.join(frontend_build_dir, "index.html"))

app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_middleware(GetAcceptLanguageMiddleware)