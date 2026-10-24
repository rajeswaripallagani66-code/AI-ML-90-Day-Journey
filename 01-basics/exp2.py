import os
os.environ["KMP_AFFINITY"] = "disabled"
os.environ["MLFLOW_TRACKING_URI"] = "sqlite:///C:/mlflow_data/mlflow.db"

import mlflow
import optuna
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

mlflow.set_tracking_uri("sqlite:///C:/mlflow_data/mlflow.db")
mlflow.set_experiment("iris-optuna-day2")

iris = load_iris()
X, y = iris.data, iris.target

def objective(trial):
    n_estimators = trial.suggest_int("n_estimators", 10, 200)
    max_depth = trial.suggest_int("max_depth", 2, 10)
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    score = cross_val_score(clf, X, y, cv=3).mean()
    return score

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=10)

print(f"best score: {study.best_value}")
print(f"best params: {study.best_params}")

with mlflow.start_run():
    mlflow.log_params(study.best_params)
    mlflow.log_metric("best_cv_score", study.best_value)
    print("Logged to MLflow!")
    