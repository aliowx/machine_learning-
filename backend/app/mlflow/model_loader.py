import mlflow
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("car_model_experiment")


def log_model_and_metrics(model, accuracy: float):
    with mlflow.start_run():
        mlflow.log_param("model_type", type(model).__name__)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")
