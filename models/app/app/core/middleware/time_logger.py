from time import time 
import logging
from fastapi import Response, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


from app.app.core.config import settings

logger = logging.getLogger(__name__)



class TimeLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint, conf=settings
    ) -> Response:
        start_time = time()
        response = await call_next(request)
        logger.info(f"[ {request.method}:{request.url} in  {time() - start_time:.3f} ms ]")

        return response
