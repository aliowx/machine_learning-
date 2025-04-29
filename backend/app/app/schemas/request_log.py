from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RequestLogInDBBase(BaseModel):
    id: int
    created: datetime
    modified: datetime
    model_config = ConfigDict(from_attributes=True)


class RequestLogCreate(BaseModel):
    request: str = None
    response: str = None
    service_name: str = None
    method: str = None
    user_id: str | None = None
    ip: str | None = None
    trace: str | None = None
    processing_time: float | None = None
    tracker_id: str | None = None


class RequestLogUpdate(BaseModel):
    pass
