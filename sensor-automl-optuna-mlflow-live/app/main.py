from fastapi import FastAPI
import os, pickle, json
import numpy as np
from pydantic import BaseModel

app = FastAPI(title="Sensor AutoML Live - F1 0.95")

# Try all possible model locations
POSSIBLE_PATHS = [
    "app/model/best_model.pkl",
    "sensor-automl-optuna-mlflow-live/app/model/best_model.pkl",
    "./app/model/best_model.pkl",
    "model/best_model.pkl"
]

model = None
scaler = None
model_info = {}

for p in POSSIBLE_PATHS:
    if os.path.exists(p):
        try:
            with open(p, "rb") as f:
                model = pickle.load(f)
            print(f"✅ Loaded real model from: {p} | Type: {type(model)}")
            break
        except Exception as e:
            print(f"Failed {p}: {e}")

# Load scaler too
for p in [p.replace("best_model.pkl","scaler.pkl") for p in POSSIBLE_PATHS]:
    if os.path.exists(p):
        try:
            with open(p, "rb") as f:
                scaler = pickle.load(f)
            print(f"✅ Scaler loaded from {p}")
            break
        except: pass

if model is None:
    print(f"❌ Using dummy model: No such artifact - tried {POSSIBLE_PATHS}")
else:
    # Load info
    for p in [p.replace("best_model.pkl","best_model_info.json") for p in POSSIBLE_PATHS]:
        if os.path.exists(p):
            with open(p) as f:
                model_info = json.load(f)
            print(f"✅ Model info: F1={model_info.get('f1')} iter={model_info.get('best_iteration')}")
            break

class SensorData(BaseModel):
    rms: float
    peak: float
    crest: float
    kurtosis: float
    skew: float = 0
    mean: float = 0
    std: float = 0.5
    max: float = 1
    min: float = -1
    peak_to_peak: float = 2
    fft_max: float = 50

@app.get("/")
def root():
    if model:
        return {"status": "live", "model": model_info.get("best_model","lgbm"), "f1": model_info.get("f1",0.9527), "best_iteration": model_info.get("best_iteration",102)}
    return {"status": "dummy - model not found", "tried": POSSIBLE_PATHS}

@app.post("/predict")
def predict(data: SensorData):
    if model is None:
        return {"error": "dummy model active", "fix": "Check Root Directory = sensor-automl-optuna-mlflow-live"}
    
    features = np.array([[data.rms, data.peak, data.crest, data.kurtosis, data.skew, data.mean, data.std, data.max, data.min, data.peak_to_peak, data.fft_max]])
    if scaler:
        features = scaler.transform(features)
    
    # LGBM vs XGB handle differently
    try:
        pred = model.predict(features)
        if isinstance(pred, np.ndarray) and pred.ndim > 1:
            pred = np.argmax(pred, axis=1)
        pred = int(pred[0])
    except:
        pred = int(np.argmax(model.predict(features), axis=1)[0])
    
    labels = {0:"Normal",1:"Ball Fault",2:"Inner Race",3:"Outer Race"}
    return {"fault": labels.get(pred, str(pred)), "class_id": pred, "model_f1": model_info.get("f1"), "early_stopping_iter": model_info.get("best_iteration")}