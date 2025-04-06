from contextvars import ContextVar

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

REQUEST_ACCEPT_LANGUAGE_KEY = "request_accept_language"



_request_accept_language_var: ContextVar[str] = ContextVar(REQUEST_ACCEPT_LANGUAGE_KEY, default='fa')


def get_accept_language():
    return _request_accept_language_var.get()



class GetAcceptLanguageMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint 
        
    )-> Response:
        accept_language = request.headers.get("Accept-Language", "fa")
        _request_accept_language_var.set(accept_language)
        response = await call_next(request)
        return response
