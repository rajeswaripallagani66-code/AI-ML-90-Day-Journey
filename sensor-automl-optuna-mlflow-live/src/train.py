import pandas as pd, xgboost as xgb, os, joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow

os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("sqlite:///mlflow.db")

df = pd.read_csv("data/processed/features.csv")
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("sensor-bearing")

with mlflow.start_run():
    model = xgb.XGBClassifier(n_estimators=50, max_depth=5, eval_metric='mlogloss', verbosity=0)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Accuracy: {acc:.4f}")
    
    mlflow.log_param("n_estimators", 50)
    mlflow.log_param("max_depth", 5)
    mlflow.log_metric("accuracy", acc)
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")
    print("Model saved to models/model.pkl + MLflow logged")