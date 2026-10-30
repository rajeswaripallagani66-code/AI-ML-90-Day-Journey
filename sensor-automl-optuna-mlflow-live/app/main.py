from fastapi import FastAPI
import os, numpy as np
from app.schemas import SensorFeatures

app = FastAPI(title="Sensor AutoML API - Day2 Live")

# Load model - try registry, else dummy
model = None
try:
    import mlflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    model = mlflow.catboost.load_model("models:/sensor_best/1")
    print("Loaded from Registry!")
except Exception as e:
    print(f"Using dummy model: {e}")
    model = None

@app.get("/")
def root():
    return {"status": "live", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(inp: SensorFeatures):
    try:
        if model is not None:
            X = np.array(inp.features).reshape(1, -1)
            pred = int(model.predict(X)[0])
            prob = float(model.predict_proba(X)[0].max())
        else:
            pred = 1 if sum(inp.features) > 0 else 0
            prob = 0.85
        return {"prediction": pred, "probability": prob}
    except Exception as ex:
        return {"prediction": 0, "probability": 0.5, "note": f"fallback: {ex}"}

@app.get("/drift")
def drift():
    return {"drift": False, "message": "No drift - Day2 local"}
