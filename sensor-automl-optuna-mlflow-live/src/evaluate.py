import os
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")

import pandas as pd, joblib
from sklearn.metrics import accuracy_score

model = joblib.load("models/model.pkl")
df = pd.read_csv("data/processed/features.csv")
acc = accuracy_score(df["label"], model.predict(df.drop("label", axis=1)))
print(f"Final Eval Accuracy: {acc:.4f}")
with mlflow.start_run():
    mlflow.log_metric("final_accuracy", acc)