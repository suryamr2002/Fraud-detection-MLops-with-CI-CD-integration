# 🚀 Quick Start Guide

## Step 1: Test API Locally

### 1.1 Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.2 Run the API
```bash
uvicorn api.main:app --reload
```

The API will start at: **http://localhost:8000**

### 1.3 Test the API
Open a **new terminal** and run:
```bash
python test_local.py
```

Or manually test:
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs
- Metrics: http://localhost:8000/metrics

---

## Step 2: Set Up Git & Push to GitHub

### 2.1 Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: Fraud Detection MLOps pipeline"
```

### 2.2 Connect to GitHub Repository
```bash
# Add your remote (replace with your repo URL)
git remote add origin https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration.git

# Or if you need to authenticate:
git remote add origin https://<your-token>@github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration.git
```

### 2.3 Push to GitHub
```bash
git branch -M main
git push -u origin main
```

**Note:** If you get authentication errors:
1. Generate a Personal Access Token: https://github.com/settings/tokens
2. Use token as password when prompted
3. Or use: `git remote set-url origin https://<token>@github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration.git`

---

## Step 3: Watch GitHub Actions Build

1. Go to: https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration/actions
2. You should see a workflow running: **"Build and Push Fraud Detection API Image"**
3. Click on it to see the build progress
4. Wait for it to complete (usually 2-5 minutes)

**What it does:**
- ✅ Builds Docker image
- ✅ Pushes to GitHub Container Registry (GHCR)
- ✅ Image available at: `ghcr.io/suryamr2002/fraud-detection-mlops-with-ci-cd-integration:latest`

---

## Step 4: Verify Docker Image

After the workflow completes:

1. Go to: https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration/pkgs/container/fraud-detection-mlops-with-ci-cd-integration
2. You should see your Docker image listed
3. Make sure it's set to **Public** (or configure imagePullSecrets for private)

---

## Step 5: Deploy to Kubernetes

Follow the `DEPLOYMENT.md` guide to:
1. Deploy Prometheus + Grafana
2. Deploy the Fraud Detection API
3. Set up HPA for auto-scaling
4. Run load tests

---

## 🔧 Troubleshooting

### API won't start locally
- Check if port 8000 is already in use
- Verify `mlruns` folder exists with your model
- Check the RUN_ID in `api/main.py` matches your MLflow run

### Git push fails
- Make sure you're authenticated to GitHub
- Check remote URL is correct
- Try using a Personal Access Token instead of password

### GitHub Actions fails
- Check the workflow logs for errors
- Verify Dockerfile is correct
- Make sure all files are committed and pushed

---

## 📝 Next Steps

Once everything is working:
1. ✅ Local API tested
2. ✅ Code pushed to GitHub
3. ✅ Docker image built in GitHub Actions
4. → Deploy to Kubernetes (see DEPLOYMENT.md)
5. → Run load tests
6. → Capture screenshots for resume

---

**Need help?** Check the error messages and refer to DEPLOYMENT.md for detailed steps.

