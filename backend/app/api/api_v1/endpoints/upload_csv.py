from typing import Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.celery.worker import process_csv_task
from app import models, schemas
from app.api import deps
from app.log import log
from celery.result import AsyncResult
from app.core.celery_app import celery_app
import io 


router = APIRouter()


@router.post("/process-csv/")
async def upload_csv(
    file: UploadFile = File(...),
    _: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    try:
        contents = await file.read()
        csv_content = contents.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    
    task = celery_app.send_task("process_csv_task", args=[csv_content])

    return {"task_id": task.id, "status": "submitted"}


@router.get("/task-status/{task_id}")
def get_status(task_id: int):...
    