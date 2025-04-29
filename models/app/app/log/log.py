import json
import logging
import time
from typing import Callable

from fastapi import BackgroundTasks, Request
from fastapi.responses import Response
from fastapi.routing import APIRoute

from app.app import crud, exceptions, schemas
from app.app.db import session


logger = logging.getLogger(__name__)


async def save_request_log_async(
    request: Request, response: Response = None, trace_back: str = ""
) -> None:
    client_host = request.client.host
    service_name = request.url.path
    method = request.method
    request_data = {
        "body": {},
        "path_params": str(request.path_params),
        "query_params": str(request.query_params),
    }

    response_data = ""
    if response:
        if "json" not in response.headers.get("content-type", ""):
            response_data = json.dumps(dict(response.headers))
        else:
            response_data = str(response.body)

    try:
        request_data["body"] = await request.json()
    except Exception:
        pass

    request_log_data = {
        "service_name": service_name,
        "method": method,
        "ip": client_host,
        "request": json.dumps(request_data),
        "response": response_data,
        "trace": trace_back,
        "processing_time": round(time.time() - request.state.start_time, 4),
    }

    try:
        request_log_data.update({"user_id": request.state.user_id})
    except:
        pass

    try:
        request_log_data.update({"tracker_id": str(request.state.tracker_id)})
    except:
        pass

    try:
        request_log_in = schemas.RequestLogCreate(**request_log_data)

        async with session.async_session() as db:
            await crud.request_log.create(db=db, obj_in=request_log_in)
            await db.commit()

    except Exception as e:
        logger.error(f"save request log err: {type(e)}, {e}")


class LogRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request.state.start_time = time.time()
            try:
                response: Response = await original_route_handler(request)
            except Exception as e:
                response = await exceptions.handle_exception(request, e)

            if not response.background:
                tasks = BackgroundTasks()
                tasks.add_task(save_request_log_async, request, response)
                response.background = tasks
            else:
                response.background.add_task(save_request_log_async, request, response)
            return response

        return custom_route_handler