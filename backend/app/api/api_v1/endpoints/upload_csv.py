from typing import Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.celery.worker import process_csv_task
from app import models, schemas
from app.api import deps
from app.log import log

router = APIRouter()


@router.post("/process-csv/")
async def upload_csv(
    file: UploadFile = File(...),
    _: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    csv_str = contents.decode("utf-8")

    task = process_csv_task.delay(csv_str)

    return {"task_id": task.id, "status": "submitted"}