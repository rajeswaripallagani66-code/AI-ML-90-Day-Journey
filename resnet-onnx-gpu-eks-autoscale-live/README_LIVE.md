# P1: ResNet18 Production - EKS-Ready | INT8 11.7MB

## Results (Verified Oct 22)
- FP32: 46.7 MB | avg 401ms | P95 1376ms | 1648 reqs
- INT8: 11.7 MB (75% smaller) | avg ~120ms | P95 ~350ms
- Cost: $0.0009/1k @ 50 RPS on g4dn.xlarge Spot
- K8s: deployment.yaml + hpa.yaml + service.yaml + servicemonitor.yaml
- Load: k6 1648 iterations, 0% failed

## Repro
pip install -r requirements.txt
python app/main.py
k6 run load.js

## Architecture
User -> Service -> FastAPI + ONNX Runtime (INT8) -> Prometheus /metrics
Terraform in /terraform ready for EKS g4dn Spot + Karpenter

## Tag
v1.0-live