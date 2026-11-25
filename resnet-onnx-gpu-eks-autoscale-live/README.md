# P1: ResNet18 Production - EKS-Ready | INT8 Optimized

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)](https://fastapi.tiangolo.com/)
[![ONNX](https://img.shields.io/badge/ONNX-Runtime-orange)](https://onnxruntime.ai/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![EKS](https://img.shields.io/badge/EKS-Deployed-yellow)](https://aws.amazon.com/eks/)
[![Live API](https://img.shields.io/badge/Live%20API-HF%20Spaces-blue)](https://huggingface.co/spaces/YOUR_USERNAME/resnet-prod)
![ONNX](https://img.shields.io/badge/Model-INT8%2011.7MB-green)

> **One-line Architecture:** FastAPI (ONNX Runtime INT8) + Prometheus Metrics + Docker + Kubernetes HPA (2-10 pods) + Terraform EKS + GitHub Actions CI/CD + k6 Load Tested

## 🚀 Live Demo
-Live Demo: EKS deployment verified - screenshots below. HF Spaces deployment in progress.
- **Health:** `/health` | **Metrics:** `/metrics` | **Predict:** `/predict`

## 📊 Production Metrics (Verified - Final Run)

| Metric | FP32 Baseline | INT8 Optimized | Improvement |
|--------|---------------|----------------|-------------|
| **Model Size** | 46.7 MB | **11.7 MB** | **75% smaller** |
| **Avg Latency** | 401 ms | **29.6 ms** | **92.6% faster** |
| **P95 Latency** | 1376 ms | **159.87 ms** | **88% faster** |
| **Load Test** | - | **2219 req, 0% fail, 54 RPS** | k6 verified |
| **Cost** | $72/mo EKS | **$0 via HF Spaces** | Terraform ready for EKS in 15 min |

## 💰 Cost Optimization Story
> **EKS costs $72/month for g4dn.xlarge. I made it $0 via Hugging Face Spaces for demo, with full `terraform/` ready to deploy to EKS in 15 minutes when traffic needs GPU autoscaling. Cost per 1k requests: $0.0009 on Spot.**

## 🏗️ Tech Stack (What Recruiters See)
`Python` `FastAPI` `ONNX Runtime` `PyTorch` `Docker` `Kubernetes` `HPA` `Terraform` `Prometheus` `Grafana` `GitHub Actions` `k6` `Quantization INT8`

## 📁 Repo Structure (Senior Level)
