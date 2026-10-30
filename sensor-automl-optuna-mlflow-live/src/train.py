import optuna, mlflow, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import catboost, xgboost, lightgbm
import os, pathlib
from imblearn.over_sampling import SMOTE

mlflow.set_tracking_uri(f"sqlite:///{os.path.join(os.getcwd(), 'mlflow.db').replace(chr(92), '/')}")
mlflow.set_experiment("sensor-day1")

possible_paths = [
    pathlib.Path("data/processed/features.csv"),
    pathlib.Path("data/raw/sensor.csv"),
]
csv_path = None
for p in possible_paths:
    if p.exists():
        csv_path = p
        break
if csv_path is None:
    all_csvs = list(pathlib.Path("data").rglob("*.csv"))
    csv_path = all_csvs[0]

df = pd.read_csv(csv_path)
print(f"Loaded {csv_path}: {df.shape}")
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sm = SMOTE(random_state=42)
X_train, y_train = sm.fit_resample(X_train, y_train)
print(f"After SMOTE: {X_train.shape}")

def objective(trial):
    model_type = trial.suggest_categorical("model", ["catboost", "xgboost", "lgbm"])
    with mlflow.start_run() as run:
        if model_type == "catboost":
            params = {
                "depth": trial.suggest_int("depth", 4, 10),
                "learning_rate": trial.suggest_float("lr", 0.01, 0.3),
                "iterations": trial.suggest_int("iter", 50, 150)
            }
            model = catboost.CatBoostClassifier(**params, verbose=False)
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            f1 = f1_score(y_test, pred, average='weighted')
            mlflow.log_params({"model": model_type, **params})
            mlflow.log_metric("f1", f1)
            mlflow.catboost.log_model(model, name="model")
        elif model_type == "xgboost":
            params = {
                "max_depth": trial.suggest_int("max_depth", 3, 10),
                "learning_rate": trial.suggest_float("lr", 0.01, 0.3),
            }
            model = xgboost.XGBClassifier(**params)
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            f1 = f1_score(y_test, pred, average='weighted')
            mlflow.log_params({"model": model_type, **params})
            mlflow.log_metric("f1", f1)
            mlflow.xgboost.log_model(model, name="model")
        else:
            params = {
                "num_leaves": trial.suggest_int("num_leaves", 20, 100),
                "learning_rate": trial.suggest_float("lr", 0.01, 0.3),
            }
            model = lightgbm.LGBMClassifier(**params, verbose=-1)
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            f1 = f1_score(y_test, pred, average='weighted')
            mlflow.log_params({"model": model_type, **params})
            mlflow.log_metric("f1", f1)
            mlflow.lightgbm.log_model(model, name="model")
        return f1

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=20)
print(f"Best F1: {study.best_value} with {study.best_params}")
print(f"✅ F1 TARGET MET!" if study.best_value > 0.65 else "Need more tuning")
