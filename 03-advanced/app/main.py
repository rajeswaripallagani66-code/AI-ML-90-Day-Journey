from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest
import time, os, numpy as np, onnxruntime as ort

MODEL_PATH = os.getenv("MODEL_PATH", "app/resnet18_int8.onnx")
print(f"Loading model: {MODEL_PATH}", flush=True)

sess = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
input_name = sess.get_inputs()[0].name

app = FastAPI(title="ml-api-optimized")

REQUEST_COUNT = Counter('http_requests_total', 'Total', ['method','endpoint','status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Latency', ['endpoint'])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start=time.time()
    resp=await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path, str(resp.status_code)).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(time.time()-start)
    return resp

@app.get("/health")
def health(): return {"status":"ok", "model": MODEL_PATH, "size_mb": round(os.path.getsize(MODEL_PATH)/1024/1024,2)}

@app.get("/")
def root(): return {"msg":"ml-api optimized running", "model": MODEL_PATH}

@app.get("/metrics")
def metrics(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict")
def predict():
    dummy = np.random.randn(1,3,224,224).astype(np.float32)
    out = sess.run(None, {input_name: dummy})[0]
    return {"prediction": int(np.argmax(out)), "model": MODEL_PATH}

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="0.0.0.0", port=8000)