import base64
import datetime
import json
import uuid
from typing import Any

from pydantic import BaseModel


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, BaseModel):
            return obj.model_dump()
        elif isinstance(obj, bytes):
            return base64.b64encode(obj).decode()
        return super(CustomJSONEncoder, self).default(obj)


class CustomJSONDecoder(json.JSONDecoder):
    pass
