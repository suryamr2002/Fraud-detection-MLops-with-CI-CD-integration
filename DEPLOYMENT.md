# Fraud Detection MLOps - Deployment Guide

## 🎯 Overview

This guide walks you through deploying the Fraud Detection ML API with full MLOps pipeline:
- ✅ Kubernetes deployment with auto-scaling (HPA)
- ✅ Prometheus monitoring
- ✅ Grafana dashboards
- ✅ CI/CD with GitHub Actions
- ✅ Load testing

---

## 📋 Prerequisites

1. **Kubernetes Cluster** (choose one):
   - **GKE** (Google Kubernetes Engine)
   - **EKS** (Amazon Elastic Kubernetes Service)
   - **AKS** (Azure Kubernetes Service)
   - **Local**: Minikube, Kind, or Docker Desktop K8s

2. **kubectl** configured to access your cluster
3. **GitHub repository** with Actions enabled

---

## 🚀 Step-by-Step Deployment

### Step 1: Build and Push Docker Image (CI/CD)

The GitHub Actions workflow automatically builds and pushes to GitHub Container Registry (GHCR) on every push to `main`.

**First time setup:**
1. Push your code to GitHub
2. The workflow will build and push: `ghcr.io/suryamr2002/fraud-detection-mlops-with-ci-cd-integration:latest`

**Verify:**
- Go to: https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration/actions
- Check that the workflow completed successfully
- Image is available at: `ghcr.io/suryamr2002/fraud-detection-mlops-with-ci-cd-integration`

---

### Step 2: Deploy Monitoring Stack (Prometheus + Grafana)

```bash
# Create monitoring namespace
kubectl apply -f k8s/monitoring/namespace.yaml

# Deploy Prometheus
kubectl apply -f k8s/monitoring/prometheus-config.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml
kubectl apply -f k8s/monitoring/prometheus-service.yaml

# Deploy Grafana
kubectl apply -f k8s/monitoring/grafana-datasources.yaml
kubectl apply -f k8s/monitoring/grafana-dashboards.yaml
kubectl apply -f k8s/monitoring/grafana-dashboard-config.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml
kubectl apply -f k8s/monitoring/grafana-service.yaml
```

**Verify:**
```bash
# Check pods
kubectl get pods -n monitoring

# Check services
kubectl get svc -n monitoring
```

---

### Step 3: Deploy Fraud Detection API

```bash
# Deploy API
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Deploy HPA (Horizontal Pod Autoscaler)
kubectl apply -f k8s/hpa.yaml
```

**Verify:**
```bash
# Check deployment
kubectl get deployment fraud-api
kubectl get pods -l app=fraud-api

# Check HPA
kubectl get hpa fraud-api-hpa

# Check service
kubectl get svc fraud-api-service
```

---

### Step 4: Access Services

#### Option A: Port Forward (for local/testing)

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

#### Option B: NodePort (for cloud)

If using NodePort (already configured):
- Grafana: `<node-ip>:30030`
- Prometheus: Expose via NodePort or LoadBalancer
- API: Expose via NodePort or LoadBalancer

#### Option C: LoadBalancer (for cloud)

Update service types to `LoadBalancer`:
```yaml
# In service.yaml files, change:
type: LoadBalancer
```

---

### Step 5: Verify Prometheus Scraping

1. Open Prometheus UI: http://localhost:9090
2. Go to **Status → Targets**
3. Verify `fraud-api` job shows as **UP**
4. Test query: `rate(predictions_total[1m])`

---

### Step 6: Access Grafana Dashboard

1. Open Grafana: http://localhost:3000
2. Login: `admin` / `admin`
3. Go to **Dashboards → Fraud Detection API - Real-Time Monitoring**
4. You should see:
   - Requests/sec
   - P95 Latency
   - Pod Count
   - Error Rate
   - CPU/Memory usage

---

### Step 7: Load Testing

Install dependencies:
```bash
pip install aiohttp
```

Run load test:
```bash
# Basic test (50 req/s for 5 minutes)
python load_test.py --url http://localhost:8000 --duration 300 --rate 50

# Heavy load (100 req/s for 10 minutes)
python load_test.py --url http://localhost:8000 --duration 600 --rate 100 --concurrency 20
```

**Watch auto-scaling:**
```bash
# In another terminal, watch pods scale
watch kubectl get pods -l app=fraud-api

# Watch HPA
watch kubectl get hpa fraud-api-hpa
```

**Expected behavior:**
- Pods scale from 2 → up to 10 as CPU/memory increases
- Grafana dashboard shows pod count increasing
- Latency should remain stable as pods scale

---

## 🔧 Troubleshooting

### Pods not starting
```bash
# Check pod logs
kubectl logs -l app=fraud-api

# Check events
kubectl describe pod <pod-name>
```

### Prometheus not scraping
```bash
# Check Prometheus config
kubectl get configmap prometheus-config -n monitoring -o yaml

# Check Prometheus logs
kubectl logs -n monitoring -l app=prometheus
```

### Image pull errors
```bash
# If using GHCR, ensure image is public or configure imagePullSecrets
# For private images, create secret:
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<github-token> \
  --docker-email=<email>

# Add to deployment.yaml:
spec:
  template:
    spec:
      imagePullSecrets:
        - name: ghcr-secret
```

### HPA not scaling
```bash
# Check HPA status
kubectl describe hpa fraud-api-hpa

# Check metrics server (required for HPA)
kubectl top nodes
kubectl top pods
```

---

## 📊 Monitoring Queries

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

# CPU usage
rate(container_cpu_usage_seconds_total{pod=~"fraud-api.*"}[1m]) * 100

# Memory usage
container_memory_usage_bytes{pod=~"fraud-api.*"} / 1024 / 1024
```

---

## 🎯 Resume Points

After deployment, you can demonstrate:

1. **Auto-scaling**: Run load test, show pods scaling from 2→10
2. **Monitoring**: Grafana dashboard with real-time metrics
3. **CI/CD**: Show GitHub Actions building/pushing images
4. **Kubernetes**: Show deployments, services, HPA
5. **Load Testing**: Show stress test results and system handling load

---

## 📝 Next Steps

1. **Production Hardening**:
   - Add Ingress controller
   - Configure TLS/SSL
   - Set up persistent storage for Prometheus/Grafana
   - Add alerting rules

2. **Advanced Features**:
   - Custom metrics for HPA
   - Canary deployments
   - Blue-green deployments
   - Multi-region deployment

---

## 🔗 Useful Commands

```bash
# Scale deployment manually
kubectl scale deployment fraud-api --replicas=5

# Update deployment
kubectl set image deployment/fraud-api fraud-api=ghcr.io/...:v2

# View logs
kubectl logs -f -l app=fraud-api

# Delete everything
kubectl delete -f k8s/
kubectl delete -f k8s/monitoring/
```

---

## 📸 Screenshots to Capture

For your resume/demo:
1. Grafana dashboard showing metrics
2. Kubernetes dashboard showing pods scaling
3. HPA status showing current/target replicas
4. Load test results
5. GitHub Actions workflow success
6. Prometheus targets page

---

**Questions?** Check the code comments in each YAML file for detailed explanations!

