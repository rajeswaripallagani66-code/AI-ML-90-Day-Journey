# AI-ML-90-Day-Journey 🚀 | Day 90 DONE

**Final Project:** ResNet18 → ONNX → FastAPI Live API

Live Proof: Siamese cat → `tabby` 200 OK

## What I Built Today
- Converted PyTorch ResNet18 to ONNX (industry standard)
- FastAPI with `/predict` endpoint + Swagger docs
- Tested with Siamese cat image - working!

## Run
```bash
cd 03-advanced
pip install -r requirements.txt
uvicorn app.main:app --reload
# Open http://localhost:8000/docs
