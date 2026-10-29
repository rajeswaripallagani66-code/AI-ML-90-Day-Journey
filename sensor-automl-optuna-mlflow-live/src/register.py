import mlflow, os
from mlflow import MlflowClient

mlflow.set_tracking_uri(f"sqlite:///{os.path.join(os.getcwd(), 'mlflow.db').replace(chr(92), '/')}")
client = MlflowClient()
exp = client.get_experiment_by_name("sensor-day1")

runs = client.search_runs(exp.experiment_id, order_by=["metrics.f1 DESC"])
best_run_id = runs[0].info.run_id
print(f"Best Run: {best_run_id} F1: {runs[0].data.metrics['f1']}")

logged_models = client.search_logged_models(
    experiment_ids=[exp.experiment_id],
    filter_string=f"source_run_id = '{best_run_id}'"
)

if not logged_models:
    logged_models = client.search_logged_models(experiment_ids=[exp.experiment_id])

model_id = logged_models[0].model_id
model_uri = logged_models[0].model_uri
print(f"Found model_id: {model_id}")
print(f"Found model_uri: {model_uri}")

# FINAL FIX: Don't create if exists
try:
    client.create_registered_model(name="sensor_best")
    print("Created new registered model sensor_best")
except:
    print("sensor_best already exists - adding new version")

mv = client.create_model_version(name="sensor_best", source=model_uri)
print(f"SUCCESS: Registered sensor_best version {mv.version}!")