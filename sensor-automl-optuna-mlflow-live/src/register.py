import mlflow
import os
from mlflow import MlflowClient

mlflow.set_tracking_uri(f"sqlite:///{os.path.join(os.getcwd(), 'mlflow.db').replace(chr(92), '/')}")
client = MlflowClient()
exp = client.get_experiment_by_name("sensor-day1")

runs = client.search_runs(exp.experiment_id, order_by=["metrics.f1 DESC"])
best = runs[0]
best_run_id = best.info.run_id
best_f1 = best.data.metrics['f1']
print(f"Best F1: {best_f1} run: {best_run_id}")

logged_models = client.search_logged_models(experiment_ids=[exp.experiment_id], filter_string=f"run_id = '{best_run_id}'")
model_uri = f"models:/{logged_models[0].model_id}"
print(f"Registering from {model_uri}")
mlflow.register_model(model_uri, "sensor_best")
print("Registered!")