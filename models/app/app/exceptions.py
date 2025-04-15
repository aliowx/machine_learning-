import logging
import traceback
from typing import Any


from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError

from app import utils
from app.core.config import settings

logger = logging.getLogger(__name__)


class CustomHTTPException(HTTPException):
    """Custom HTTPException class for common exception handling."""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        msg_code: utils.MessageCodes = utils.MessageCodes.internal_error,
        detail: str | None = None,
        headers: dict | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.msg_code = msg_code


def get_traceback_info(exc: Exception):
    traceback_str = (traceback.format_tb(exc.__traceback__))[-1]
    traceback_full = "".join(traceback.format_tb(exc.__traceback__))
    exception_type = type(exc).__name__
    return exception_type, traceback_str, traceback_full


def create_system_exception_handler(
    status_code: str,
    msg_code: str,
):
    async def exception_handler(request: Request, exc: Any):
        exception_type, traceback_str, _ = get_traceback_info(exc)
        logger.error(f"Exception of type {exception_type}:\n{traceback_str}")

        response_data = {
            "data": str(exc.errors()),
            "msg_code": msg_code,
            "status_code": status_code,
        }

        response = utils.APIErrorResponse(**response_data)
        return response

    return exception_handler


def create_exception_handler(status_code):
    async def exception_handler(request: Request, exc: Any):
        response_data = {
            "data": str(exc.detail),
            "msg_code": exc.msg_code,
            "status_code": status_code,
        }

        response = utils.APIErrorResponse(**response_data)
        return response

    return exception_handler


async def http_exception_handler(request: Request, exc: Any):
    response = utils.APIErrorResponse(
        data=exc.detail,
        msg_code=utils.MessageCodes.internal_error,
        status_code=exc.status_code,
    )
    return response


async def internal_exceptions_handler(request: Request, exc: Any):
    exception_type, traceback_str, traceback_full = get_traceback_info(exc)
    logger.error(f"Unhandled {exception_type} Exception Happened:\n{traceback_str} \n{traceback_full}")

    error_msg = ""
    if settings.DEBUG:
        error_msg = str(exc)

    return utils.APIErrorResponse(
        data=error_msg,
        msg_code=utils.MessageCodes.internal_error,
        status_code=500,
    )


# Define custom exception classes
class ValidationException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None, headers: dict | None = None,):
        super().__init__(msg_code=msg_code, detail=detail, headers=headers)


class NotFoundException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None, headers: dict | None = None,):
        super().__init__(msg_code=msg_code, detail=detail, headers=headers)


class AlreadyExistException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None, headers: dict | None = None,):
        super().__init__(msg_code=msg_code, detail=detail, headers=headers)


class InternalErrorException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None, headers: dict | None = None,):
        super().__init__(msg_code=msg_code, detail=detail, headers=headers)


class UnauthorizedException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None, headers: dict | None = None,):
        super().__init__(msg_code=msg_code, detail=detail, headers=headers)


class ForbiddenException(CustomHTTPException):
    def __init__(self, detail: str | None = None, msg_code: utils.MessageCodes = None, headers: dict | None = None,):
        super().__init__(msg_code=msg_code, detail=detail, headers=headers)


# Create a dictionary of exception handlers
exception_handlers = {
    Exception: internal_exceptions_handler,
    HTTPException: http_exception_handler,
    ValidationException: create_exception_handler(status.HTTP_400_BAD_REQUEST),
    NotFoundException: create_exception_handler(status.HTTP_404_NOT_FOUND),
    AlreadyExistException: create_exception_handler(status.HTTP_409_CONFLICT),
    InternalErrorException: create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ),
    UnauthorizedException: create_exception_handler(status.HTTP_401_UNAUTHORIZED),
    ForbiddenException: create_exception_handler(status.HTTP_403_FORBIDDEN),
    RequestValidationError: create_system_exception_handler(
        status.HTTP_400_BAD_REQUEST, msg_code=utils.MessageCodes.bad_request
    ),
    ResponseValidationError: create_system_exception_handler(
        status.HTTP_400_BAD_REQUEST, msg_code=utils.MessageCodes.internal_error
    ),
}


async def handle_exception(request: Request, exc: Any):
    exc_type = type(exc)
    handler = exception_handlers.get(exc_type, internal_exceptions_handler)
    return await handler(request, exc)
