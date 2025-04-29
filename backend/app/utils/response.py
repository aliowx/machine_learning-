from abc import ABC
from enum import IntEnum
from typing import Any, Generic, TypeVar, no_type_check

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing_extensions import Self

from app import utils

T = TypeVar("T")


class MessageStatus(IntEnum):
    SUCCESS = 0
    FAILURE = 1


class ApiResponseHeader(BaseModel, Generic[T], ABC):
    """Header type of APIResponseType"""

    status: int = 0
    message: str = "Successful Operation"
    messageCode: int = Field(
        ..., description=str(utils.MessageCodes.english_messages_names)
    )


class PaginatedContent(BaseModel, Generic[T]):
    """Content data type for lists with pagination"""

    data: T
    total_count: int = 0
    size: int | None = None
    page: int = 1


class PaginatedContentWithAmount(BaseModel, Generic[T]):
    """Content data type for lists with pagination and total amount"""

    data: T
    total_count: int = 0
    total_amount: int = 0
    size: int = 100
    page: int = 1


class APIResponseType(BaseModel, Generic[T]):
    """
    an api response type for using as the api's router response_model
    use this for apis that use our APIResponse class for their output
    """

    header: ApiResponseHeader
    content: T | None = None


class APIResponse(APIResponseType):
    """
    Custom reponse class for apis
    Adds custom header, messages to reponses
    """

    # TODO: fix return type of APIResponse to pass typing check and not
    # raise pydantic errors
    @no_type_check
    def __new__(
        cls,
        data: T,
        *args,
        msg_code: int = 0,
        msg_status: MessageStatus = MessageStatus.SUCCESS,
        **kwargs
    ) -> Self:
        cls.header = ApiResponseHeader(
            status=msg_status,
            message=utils.MessageCodes.get_message(msg_code),
            messageCode=msg_code,
        )
        cls.content = jsonable_encoder(data)
        return {
            "header": cls.header,
            "content": cls.content,
        }


class APIErrorResponse(JSONResponse):
    """
    Custom error reponse class for apis
    Adds custom header, messages to error reponses
    """

    def __init__(
        self,
        data: Any,
        msg_code: int = utils.MessageCodes.successful_operation,
        msg_status: MessageStatus = MessageStatus.FAILURE,
        header: dict | None = None,
        **kwargs
    ) -> None:
        header_data = {
            "status": msg_status,
            "message": utils.MessageCodes.get_message(msg_code),
            "messageCode": msg_code,
        }
        if header:
            header_data = header
        self.response_data = {
            "header": header_data,
            "content": jsonable_encoder(data),
        }
        super().__init__(self.response_data, **kwargs)
