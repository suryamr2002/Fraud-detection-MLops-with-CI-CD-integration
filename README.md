# 🚀 Fraud Detection MLOps Pipeline

> **End-to-End Real-Time ML System with Full MLOps Pipeline**  
> Production-ready fraud detection API with Kubernetes, auto-scaling, monitoring, and CI/CD

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-blue)](https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration/actions)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployed-green)](https://kubernetes.io/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboard-red)](https://grafana.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Deployment](#-deployment)
- [Monitoring & Observability](#-monitoring--observability)
- [Load Testing](#-load-testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Screenshots](#-screenshots)
- [Resume Highlights](#-resume-highlights)

---

## 🎯 Overview

This project demonstrates a **production-ready MLOps pipeline** for real-time fraud detection. It includes:

- **ML Model**: Logistic Regression trained on IEEE Fraud Detection dataset
- **API**: FastAPI-based prediction service with Prometheus metrics
- **Containerization**: Docker images built via GitHub Actions
- **Orchestration**: Kubernetes with Horizontal Pod Autoscaler (HPA)
- **Monitoring**: Prometheus + Grafana for real-time observability
- **CI/CD**: Automated build and deployment pipeline
- **Load Testing**: Stress testing with auto-scaling demonstration

### Key Metrics
- **Auto-scaling**: 2-10 pods based on CPU/memory
- **Latency**: P95 < 500ms under load
- **Throughput**: 100+ requests/second
- **Availability**: High availability with multiple replicas

---

## ✨ Features

### 🔧 Core Features
- ✅ **Real-time Fraud Prediction API** - FastAPI with MLflow model serving
- ✅ **Prometheus Metrics** - Request rate, latency, error rate tracking
- ✅ **Grafana Dashboards** - Real-time visualization of system metrics
- ✅ **Kubernetes Deployment** - Production-ready container orchestration
- ✅ **Auto-scaling (HPA)** - Automatic pod scaling based on CPU/memory
- ✅ **Health Checks** - Liveness and readiness probes
- ✅ **CI/CD Pipeline** - Automated Docker builds via GitHub Actions
- ✅ **Load Testing** - Comprehensive stress testing script

### 📊 Monitoring Panels
- **Requests per Second** - Real-time request rate
- **P95 Latency** - 95th percentile response time
- **Pod Count** - Active Kubernetes pods (shows auto-scaling)
- **Error Rate** - Failed requests tracking
- **CPU/Memory Usage** - Resource utilization per pod

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  GitHub Actions (CI/CD)                              │  │
│  │  • Build Docker Image                                │  │
│  │  • Push to GHCR                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Kubernetes Cluster                              │
│                                                              │
│  ┌──────────────────┐      ┌──────────────────────────┐  │
│  │  Fraud API       │      │  Monitoring Stack        │  │
│  │  (2-10 pods)     │      │                          │  │
│  │  • FastAPI        │◄─────┤  • Prometheus            │  │
│  │  • MLflow Model   │      │  • Grafana               │  │
│  │  • Metrics        │      │  • Dashboards            │  │
│  └────────┬─────────┘      └──────────────────────────┘  │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  HPA             │                                       │
│  │  Auto-scaling    │                                       │
│  │  CPU: 70%        │                                       │
│  │  Memory: 80%     │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Load Testing    │
              │  • Stress Test   │
              │  • Auto-scaling  │
              └──────────────────┘
```

### Component Details

1. **FastAPI Application** (`api/main.py`)
   - Serves ML model predictions
   - Exposes `/predict` endpoint
   - Prometheus metrics at `/metrics`
   - Health check at `/health`

2. **Kubernetes Deployment**
   - Deployment with 2 initial replicas
   - Service for load balancing
   - HPA for auto-scaling (2-10 pods)

3. **Monitoring Stack**
   - Prometheus: Metrics collection and storage
   - Grafana: Visualization and dashboards
   - Auto-discovery of pods via Kubernetes SD

4. **CI/CD Pipeline**
   - GitHub Actions: Automated builds
   - Docker: Containerization
   - GHCR: Container registry

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10** - Core language
- **FastAPI** - Web framework
- **MLflow** - Model tracking and serving
- **scikit-learn** - Machine learning
- **pandas** - Data processing

### Infrastructure
- **Docker** - Containerization
- **Kubernetes** - Container orchestration
- **Prometheus** - Metrics collection
- **Grafana** - Visualization

### DevOps
- **GitHub Actions** - CI/CD
- **GitHub Container Registry** - Image storage
- **kubectl** - Kubernetes CLI

### Testing
- **aiohttp** - Async HTTP client for load testing
- **Python** - Load testing scripts

---

## 📁 Project Structure

```
Fraud Detection-mlops/
│
├── api/
│   └── main.py                 # FastAPI application with Prometheus metrics
│
├── k8s/                        # Kubernetes manifests
│   ├── deployment.yaml         # Fraud API deployment
│   ├── service.yaml            # Service definition
│   ├── hpa.yaml                # Horizontal Pod Autoscaler
│   └── monitoring/
│       ├── namespace.yaml
│       ├── prometheus-*.yaml   # Prometheus setup
│       └── grafana-*.yaml      # Grafana setup
│
├── training/
│   ├── training_v1.py          # Model training script
│   └── training_v1.ipynb       # Training notebook
│
├── spark/
│   └── feature_engineering.ipynb  # Feature engineering
│
├── .github/
│   └── workflows/
│       └── docker-build.yml    # CI/CD pipeline
│
├── mlruns/                     # MLflow model artifacts
│
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── load_test.py                # Load testing script
├── test_local.py               # Local API testing
│
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Kubernetes cluster (or use [Play with Kubernetes](https://labs.play-with-k8s.com/))
- kubectl configured
- Docker (for local testing, optional)

### Local Testing

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run API Locally**
   ```bash
   uvicorn api.main:app --reload
   ```

3. **Test API**
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # API docs
   # Open http://localhost:8000/docs in browser
   
   # Run test script
   python test_local.py
   ```

---

## 📦 Deployment

### Step 1: Build Docker Image (CI/CD)

The GitHub Actions workflow automatically builds and pushes the Docker image on every push to `main`.

**Image Location:**
```
ghcr.io/suryamr2002/fraud-detection-mlops-with-ci-cd-integration:latest
```

**Verify Build:**
- Check [GitHub Actions](https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration/actions)

### Step 2: Deploy to Kubernetes

#### Option A: Play with Kubernetes (Free, Recommended for Testing)

1. Go to: https://labs.play-with-k8s.com/
2. Login with GitHub
3. Create instance
4. Follow [SIMPLE_K8S_SETUP.md](SIMPLE_K8S_SETUP.md)

#### Option B: Cloud Provider (Production)

**Deploy Monitoring Stack:**
```bash
kubectl apply -f k8s/monitoring/namespace.yaml
kubectl apply -f k8s/monitoring/prometheus-*.yaml
kubectl apply -f k8s/monitoring/grafana-*.yaml
```

**Deploy Fraud Detection API:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

**Verify Deployment:**
```bash
kubectl get pods
kubectl get svc
kubectl get hpa
```

### Step 3: Access Services

**Port Forward:**
```bash
# API
kubectl port-forward svc/fraud-api-service 8000:80

# Prometheus
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Grafana
kubectl port-forward -n monitoring svc/grafana-service 3000:3000
```

**Access:**
- API: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📊 Monitoring & Observability

### Prometheus Metrics

The API exposes the following Prometheus metrics:

- `predictions_total` - Total prediction requests (Counter)
- `prediction_errors_total` - Failed requests (Counter)
- `prediction_latency_seconds` - Request latency (Histogram)
- `prediction_requests_in_progress` - Active requests (Gauge)

### Grafana Dashboard

**Dashboard: "Fraud Detection API - Real-Time Monitoring"**

**Panels:**
1. **Requests per Second** - `rate(predictions_total[1m])`
2. **P95 Latency** - `histogram_quantile(0.95, rate(prediction_latency_seconds_bucket[1m]))`
3. **Pod Count** - `count(kube_pod_info{pod=~"fraud-api.*"})`
4. **Error Rate** - `rate(prediction_errors_total[1m])`
5. **CPU Usage** - Per pod CPU utilization
6. **Memory Usage** - Per pod memory consumption

### Prometheus Queries

```promql
# Requests per second
rate(predictions_total[1m])

# P95 Latency
histogram_quantile(0.95, rate(prediction_latency_seconds_bucket[1m]))

# Pod count
count(kube_pod_info{pod=~"fraud-api.*"})

# Error rate
rate(prediction_errors_total[1m])
```

---

## 🧪 Load Testing

### Run Load Test

```bash
# Install dependencies
pip install aiohttp

# Basic test (50 req/s for 5 minutes)
python load_test.py --url http://localhost:8000 --duration 300 --rate 50

# Heavy load (100 req/s for 10 minutes)
python load_test.py --url http://localhost:8000 --duration 600 --rate 100 --concurrency 20
```

### Watch Auto-Scaling

```bash
# Terminal 1: Watch pods
watch kubectl get pods

# Terminal 2: Watch HPA
watch kubectl get hpa

# Terminal 3: Run load test
python load_test.py --url http://<api-url> --duration 300 --rate 100
```

### Expected Results

- **Initial Pods**: 2
- **Under Load**: Scales to 4-10 pods (based on CPU/memory)
- **Latency**: P95 < 500ms
- **Success Rate**: > 99%

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

**File:** `.github/workflows/docker-build.yml`

**Triggers:**
- Push to `main` branch
- Pull requests to `main`

**Steps:**
1. Checkout code
2. Set up Docker Buildx
3. Login to GitHub Container Registry
4. Build Docker image
5. Push to GHCR

**Image Tags:**
- `latest` - Latest main branch
- `main` - Main branch tag
- SHA-based tags for traceability

### Manual Deployment

```bash
# Update deployment with new image
kubectl set image deployment/fraud-api \
  fraud-api=ghcr.io/suryamr2002/fraud-detection-mlops-with-ci-cd-integration:latest

# Or apply updated deployment
kubectl apply -f k8s/deployment.yaml
```

---


## 📚 Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
- [SIMPLE_K8S_SETUP.md](SIMPLE_K8S_SETUP.md) - Quick Kubernetes setup
- [K8S_TESTING_GUIDE.md](K8S_TESTING_GUIDE.md) - Testing guide
- [QUICK_START.md](QUICK_START.md) - Quick start guide

---

## 🔧 Configuration

### Environment Variables

The API uses MLflow for model loading. Update `RUN_ID` in `api/main.py`:

```python
RUN_ID = "your-mlflow-run-id"
MODEL_URI = f"runs:/{RUN_ID}/model"
```

### Kubernetes Resources

**Deployment:**
- CPU Request: 250m
- CPU Limit: 500m
- Memory Request: 512Mi
- Memory Limit: 1Gi

**HPA:**
- Min Replicas: 2
- Max Replicas: 10
- CPU Target: 70%
- Memory Target: 80%

---

## 🐛 Troubleshooting

### Pods Not Starting
```bash
kubectl logs -l app=fraud-api
kubectl describe pod <pod-name>
```

### Prometheus Not Scraping
```bash
kubectl get configmap prometheus-config -n monitoring -o yaml
kubectl logs -n monitoring -l app=prometheus
```

### Image Pull Errors
```bash
# Check image exists
docker pull ghcr.io/suryamr2002/fraud-detection-mlops-with-ci-cd-integration:latest

# For private images, configure imagePullSecrets
```

### HPA Not Scaling
```bash
kubectl describe hpa fraud-api-hpa
kubectl top pods  # Requires metrics-server
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Surya Murugan**

- GitHub: [@suryamr2002](https://github.com/suryamr2002)
- Project Link: [Fraud Detection MLOps](https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration)

---

## 🙏 Acknowledgments

- IEEE Fraud Detection Dataset: [Kaggle Competition](https://www.kaggle.com/competitions/ieee-fraud-detection)
- MLflow for model tracking
- FastAPI for the web framework
- Kubernetes community

---

## 📊 Project Status

✅ **Complete** - Production-ready MLOps pipeline

- [x] Model training and versioning
- [x] API development with metrics
- [x] Docker containerization
- [x] Kubernetes deployment
- [x] Auto-scaling (HPA)
- [x] Monitoring (Prometheus + Grafana)
- [x] CI/CD pipeline
- [x] Load testing
- [x] Documentation

---

**⭐ If you find this project helpful, please give it a star!**

---

*Last updated: 2024*

