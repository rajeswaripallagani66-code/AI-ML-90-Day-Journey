import os
os.environ["MLFLOW_TRACKING_URI"] = "sqlite:///C:/mlflow_data/mlflow.db"

import mlflow
mlflow.set_tracking_uri("sqlite:///C:/mlflow_data/mlflow.db")

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("p1_practice")

for n in [10, 50]:
    with mlflow.start_run():
        mlflow.log_param("n_estimators", n)
        model = RandomForestClassifier(n_estimators=n, random_state=42)
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, name="rf_model")
        print(f"n={n} -> Accuracy: {acc}")