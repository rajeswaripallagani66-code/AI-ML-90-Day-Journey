import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
from mlflow.tracking import MlflowClient
client = MlflowClient()
exp = client.get_experiment_by_name("sensor-day1")
runs = client.search_runs(exp.experiment_id, order_by=["metrics.f1 DESC"])
print(f"Total runs: {len(runs)}")
for r in runs[:5]:
    print(f"F1: {r.data.metrics['f1']:.4f} - {r.data.params}")