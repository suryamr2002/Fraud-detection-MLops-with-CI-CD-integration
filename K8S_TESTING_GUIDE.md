# 🧪 Kubernetes Testing Guide

## Overview

Since you **can't install Docker/Kubernetes locally**, here's the process:

1. ✅ **Push to GitHub** → GitHub Actions builds Docker image
2. ✅ **Get Cloud K8s Cluster** → Deploy and test there
3. ✅ **Verify Everything Works** → Auto-scaling, monitoring, etc.

---

## Step 1: Push Code to GitHub (Build Docker Image)

### 1.1 Set Up Git (if not done)

```powershell
# Navigate to project
cd "C:\Users\Fraud Detection-mlops"

# Initialize git (if needed)
git init

# Add all files
git add .

# Commit
git commit -m "Add Kubernetes deployment, monitoring, and CI/CD pipeline"
```

### 1.2 Connect to GitHub

```powershell
# Add remote (if not already added)
git remote add origin https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration.git

# Or update if exists
git remote set-url origin https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration.git
```

### 1.3 Push to GitHub

```powershell
# Push to main branch
git branch -M main
git push -u origin main
```

**If authentication fails:**
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic) with `repo` permissions
3. Use token as password when prompted

### 1.4 Verify GitHub Actions

1. Go to: https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration/actions
2. Wait for workflow to complete (2-5 minutes)
3. Verify Docker image is built: `ghcr.io/suryamr2002/fraud-detection-mlops-with-ci-cd-integration:latest`

---

## Step 2: Get a Kubernetes Cluster

You need a **cloud Kubernetes cluster**. Here are options:

### Option A: Free/Cheap Cloud Providers

#### 🆓 **Google Cloud Platform (GKE) - Free Trial**
- **Free**: $300 credit for 90 days
- **Setup**: https://cloud.google.com/kubernetes-engine/docs/quickstart
- **Cost**: Free tier available, then ~$73/month for small cluster

```bash
# Install gcloud CLI
# Then create cluster:
gcloud container clusters create fraud-detection-cluster \
  --num-nodes=2 \
  --machine-type=e2-small \
  --zone=us-central1-a
```

#### 🆓 **DigitalOcean Kubernetes - $12/month**
- **Cost**: $12/month for basic cluster
- **Setup**: https://docs.digitalocean.com/products/kubernetes/quickstart/
- **Easiest**: Web UI to create cluster

#### 🆓 **Linode (Akamai) - $10/month**
- **Cost**: $10/month
- **Setup**: https://www.linode.com/docs/kubernetes/

#### 🆓 **Oracle Cloud - Always Free**
- **Free**: Always free tier available
- **Setup**: https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengettingstarted.htm

### Option B: Local Testing Alternatives (No Admin Required)

#### 🆓 **Play with Kubernetes (PWK)**
- **Free**: 4-hour sessions
- **URL**: https://labs.play-with-k8s.com/
- **Perfect for**: Quick testing, demos
- **Limitation**: Sessions expire after 4 hours

#### 🆓 **Killercoda**
- **Free**: Interactive K8s playground
- **URL**: https://killercoda.com/
- **Perfect for**: Learning and testing

### Option C: Use Existing Cluster

If you have access to:
- Company K8s cluster
- AWS EKS
- Azure AKS
- Any existing cluster

---

## Step 3: Deploy to Kubernetes

Once you have a cluster, get `kubectl` access:

### 3.1 Install kubectl

**Windows:**
```powershell
# Using Chocolatey
choco install kubernetes-cli

# Or download from:
# https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
```

### 3.2 Connect to Your Cluster

**For GKE:**
```bash
gcloud container clusters get-credentials fraud-detection-cluster --zone=us-central1-a
```

**For DigitalOcean:**
```bash
# Download kubeconfig from DigitalOcean dashboard
# Save to: C:\Users\<username>\.kube\config
```

**For Play with Kubernetes:**
- Copy the kubeconfig from the web interface
- Save to: `C:\Users\<username>\.kube\config`

### 3.3 Verify Connection

```powershell
kubectl get nodes
# Should show your cluster nodes
```

---

## Step 4: Deploy Everything

### 4.1 Deploy Monitoring Stack

```powershell
# Create namespace
kubectl apply -f k8s\monitoring\namespace.yaml

# Deploy Prometheus
kubectl apply -f k8s\monitoring\prometheus-config.yaml
kubectl apply -f k8s\monitoring\prometheus-deployment.yaml
kubectl apply -f k8s\monitoring\prometheus-service.yaml

# Deploy Grafana
kubectl apply -f k8s\monitoring\grafana-datasources.yaml
kubectl apply -f k8s\monitoring\grafana-dashboards.yaml
kubectl apply -f k8s\monitoring\grafana-dashboard-config.yaml
kubectl apply -f k8s\monitoring\grafana-deployment.yaml
kubectl apply -f k8s\monitoring\grafana-service.yaml
```

### 4.2 Deploy Fraud Detection API

```powershell
# Deploy API
kubectl apply -f k8s\deployment.yaml
kubectl apply -f k8s\service.yaml

# Deploy HPA (Auto-scaling)
kubectl apply -f k8s\hpa.yaml
```

### 4.3 Verify Deployment

```powershell
# Check pods
kubectl get pods
kubectl get pods -n monitoring

# Check services
kubectl get svc
kubectl get svc -n monitoring

# Check HPA
kubectl get hpa
```

---

## Step 5: Test the Deployment

### 5.1 Access Services

**Port Forward (for testing):**
```powershell
# API (Terminal 1)
kubectl port-forward svc/fraud-api-service 8000:80

# Prometheus (Terminal 2)
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Grafana (Terminal 3)
kubectl port-forward -n monitoring svc/grafana-service 3000:3000
```

**Access:**
- API: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

### 5.2 Test API

```powershell
# Health check
curl http://localhost:8000/health

# Or use test script
python test_local.py
```

### 5.3 Test Auto-Scaling

```powershell
# Watch pods while running load test
kubectl get pods -w

# In another terminal, run load test
python load_test.py --url http://localhost:8000 --duration 300 --rate 100

# Watch HPA
kubectl get hpa -w
```

**Expected:**
- Pods scale from 2 → up to 10
- CPU/Memory increases trigger scaling
- Grafana shows pod count increasing

---

## Step 6: Verify Everything Works

### ✅ Checklist

- [ ] GitHub Actions built Docker image successfully
- [ ] Kubernetes cluster accessible via `kubectl`
- [ ] All pods running (`kubectl get pods`)
- [ ] API accessible at http://localhost:8000/docs
- [ ] Prometheus scraping metrics (check http://localhost:9090/targets)
- [ ] Grafana dashboard showing metrics
- [ ] HPA scaling pods under load
- [ ] Load test completes successfully

---

## 🎯 Recommended Approach for You

Since you can't install locally:

1. **✅ Push to GitHub NOW** → Build Docker image
2. **✅ Use Play with Kubernetes (PWK)** → Free, no install needed
   - Go to: https://labs.play-with-k8s.com/
   - Create 4-hour session
   - Deploy and test everything
   - Perfect for demos/resume

3. **OR Use DigitalOcean** → $12/month, easiest setup
   - Create cluster via web UI
   - Download kubeconfig
   - Deploy and test

---

## 📸 Screenshots to Capture

For your resume:
1. ✅ GitHub Actions workflow success
2. ✅ `kubectl get pods` showing running pods
3. ✅ Grafana dashboard with metrics
4. ✅ HPA showing scaling (before/after load test)
5. ✅ Load test results

---

## 🚀 Quick Start (Recommended)

**Right Now:**
1. Push code to GitHub (see Step 1 above)
2. Wait for GitHub Actions to build image
3. Go to: https://labs.play-with-k8s.com/
4. Create session → Deploy → Test → Screenshot

**For Production Demo:**
- Use DigitalOcean or GKE
- More stable, longer-term testing

---

**Questions?** Let me know which option you want to use!

