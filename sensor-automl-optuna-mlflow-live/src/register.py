import os
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
print(f"MLflow tracking: {mlflow.get_tracking_uri()} - OK")