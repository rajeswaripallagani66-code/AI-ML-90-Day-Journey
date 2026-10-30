# Sensor AutoML — P2 Live Production 🚀

**Live API:** https://sensor-automl-live.onrender.com
**Docs:** https://sensor-automl-live.onrender.com/docs
**Model:** LightGBM (Optuna tuned) — F1: 0.9526 | Best Iter: 102

## Architecture
Sensor Data → Feature Engineering (11 features) → LightGBM (0.95 F1) → FastAPI → Docker → Render (Free $0)

## Live Endpoints
- `GET /` → status live, model, f1
- `GET /health` → health check
- `POST /predict` → {rms, peak, crest...} → Normal/Fault

## Performance
- Model: LGBM Booster, 0.9526 F1
- Latency: <100ms p95 (k6 tested)
- Deploy: Docker + libgomp1 fix, Uvicorn on Render

## Run Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload