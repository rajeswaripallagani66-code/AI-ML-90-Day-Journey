import pandas as pd, os, optuna, mlflow
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("sensor-day1")

df = pd.read_csv("data/processed/features.csv")
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def run_model(model_name):
    def objective(trial):
        with mlflow.start_run(nested=True):
            if model_name == "xgb":
                params = {
                    "n_estimators": trial.suggest_int("n_estimators", 50, 300),
                    "max_depth": trial.suggest_int("max_depth", 3, 10),
                    "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3)
                }
                model = xgb.XGBClassifier(**params, eval_metric='mlogloss', verbosity=0)
            elif model_name == "lgbm":
                params = {
                    "n_estimators": trial.suggest_int("n_estimators", 50, 300),
                    "max_depth": trial.suggest_int("max_depth", 3, 10),
                    "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3)
                }
                model = lgb.LGBMClassifier(**params, verbose=-1)
            else:
                params = {
                    "depth": trial.suggest_int("depth", 4, 10),
                    "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
                    "iterations": trial.suggest_int("iterations", 50, 300)
                }
                model = CatBoostClassifier(**params, verbose=False)

            model.fit(X_train, y_train)
            f1 = f1_score(y_test, model.predict(X_test), average='weighted')
            mlflow.log_params(params)
            mlflow.log_metric("f1", f1)
            mlflow.log_param("model_name", model_name)
            return f1

    with mlflow.start_run(run_name=f"{model_name}-parent"):
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=20)
        print(f"{model_name} BEST F1: {study.best_value:.4f}")

# 60 runs total
for m in ["xgb", "lgbm", "catboost"]:
    run_model(m)

print("Day1 DONE - 60 runs logged")