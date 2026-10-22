from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest
import time

print("Starting ml-api v2-metrics NO-ONNX", flush=True)

app = FastAPI()

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
def health():
    return {"status":"ok"}

@app.get("/")
def root():
    return {"msg":"ml-api v2-metrics running"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict")
def predict(data: dict):
    return {"prediction": "ok", "input": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)