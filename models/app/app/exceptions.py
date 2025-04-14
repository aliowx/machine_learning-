import logging 
import traceback
from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestErrorModel, ResponseValidationError

from app import utils  
from app.core.config import settings



logger = logging.getLogger(__name__)



class CustomHTTPException(HTTPException):
    """Custom HTTPException class for common exception handling."""
    
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        msg_code: utils.MessageCodes = utils.MessageCodes.internal_error,
        detail: str = None | None,
        headers: dict = None | None  
    )-> None:
        super().__init__(status_code=status_code,detail=detail,headers=headers)
        self.msg_code = msg_code
        
        
        
def get_traceback_info(exc: Exception):
    traceback_str = (traceback.format_tb(exc.__traceback__))[-1]
    traceback_full = "".join(traceback.format_tb(exc.__traceback__))
    exception_type = type(exc).__name__
    return traceback_str, traceback_full, exception_type



def create_system_exception_handler(
    status_code: str,
    msg_code: str
):
    async def exception_handler(request:Request, exc: Any):
        exception_type, traceback_str, _ =get_traceback_info(exc)
        logger.error(f"Exception of type {exception_type}:\n{traceback_str}")
        
        response_data = { 
            "data": str(exc.errors()),
            "msg_code":msg_code,
            "status_code":status_code
        }
        
        response = utils.APIErrorResponse(**response_data)
        return response
    
    return exception_handler



def create_exception_handler(status_code):
    async def exception_handler(request: Request, exc:Any):
        request_data = {
            'data': str(exc.detail),
            'msg_code': exc.msg_code,
            'status_code': status_code
        }
        response = utils.APIErrorResponse(**request_data)
        return response
    
    return exception_handler





async def http_exception_handler(request: Request, exc:Any):
    response = utils.APIErrorResponse(
        date=exc.detail,
        msg_code=utils.MessageCodes.internal_error,
        status_code=exc.status_code  
    )
    return response