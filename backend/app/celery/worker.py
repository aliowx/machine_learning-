import logging 
import math 
import random
from datetime import datetime, timedelta, UTC
from app.core.celery_app import DatabaseTask, celery_app
import pickle
import pandas as pd
import io


with open("model.pkl", "rb") as file:
    model = pickle.load(file)
    
    
namespace = "job worker"

logger = logging.getLogger(__name__)


@celery_app.task(
    base=DatabaseTask,
    bind=True,
    acks_late=True,
    max_retries=4,
    soft_time_limit=240,
    time_limit=360,
    name="test",
)
def test(word: str)->str:
    return f"task celery app {word}"



@celery_app.task(
    base=DatabaseTask,
    bind=True,
    acks_late=True,
    max_retries=4,
    soft_time_limit=240,
    time_limit=360,
    name="process_csv_task",
)
def process_csv_task(self, csv_content: str):
    try:
        df = pd.read_csv(io.StringIO(csv_content))

        if df.empty:
            raise ValueError("CSV file is empty")

        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
        if len(numeric_cols) != len(df.columns):
            raise ValueError("All columns must be numeric")

        logger.info(f"{namespace} - original shape: {df.shape}")
        

        if df.columns is None or len(df.columns) == 0:
            raise ValueError("No columns found in the CSV file")


        if df.isnull().values.any():
            df = df.fillna(df.mean(numeric_only=True))


        df = df.sort_values(by=df.columns[0])


        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()

        logger.info(f"{namespace} - cleaned shape: {df.shape}")

        return df.to_json(orient="records")

    except Exception as exc:
        logger.error(f"{namespace} - error occurred: {str(exc)}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
