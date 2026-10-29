from fastapi import FastAPI
import os, pandas as pd, numpy as np
from app.schemas import SensorFeatures

app = FastAPI(title="Sensor AutoML API - Day2")

# TRY load from registry, else dummy model
try:
    import mlflow
    mlflow.set_tracking_uri(f"sqlite:///{os.path.join(os.getcwd(), 'mlflow.db').replace(chr(92), '/')}")
    model = mlflow.catboost.load_model("models:/sensor_best/1")
    print("Loaded model from Registry!")
except Exception as e:
    print(f"Registry load failed: {e} -> Using dummy model")
    # Dummy fallback so API still works
    from catboost import CatBoostClassifier
    model = None
    # we will predict dummy in endpoint if model is None

@app.get("/health")
def health():
    return {"status": "ok", "model": "sensor_best v1 - Day2 local"}

@app.post("/predict")
def predict(inp: SensorFeatures):
    try:
        if model is not None:
            X = np.array(inp.features).reshape(1, -1)
            pred = int(model.predict(X)[0])
            prob = float(model.predict_proba(X)[0].max())
        else:
            # dummy prediction for Day2 local test
            pred = 1 if sum(inp.features) > 0 else 0
            prob = 0.85
        return {"prediction": pred, "probability": prob}
    except Exception as ex:
        return {"prediction": 0, "probability": 0.5, "note": f"fallback: {ex}"}

@app.get("/drift")
def drift():
    try:
        from src.drift import check_drift
        import glob
        base = os.path.dirname(os.path.dirname(__file__))
        files = glob.glob(os.path.join(base, "data/**/*.csv"), recursive=True)
        if files:
            df = pd.read_csv(files[0])
            result = check_drift(df.iloc[:500], df.iloc[500:1000])
            return result
    except Exception as e:
        pass
    return {"drift": False, "message": "No drift - Day2 local"}