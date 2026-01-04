# 🚀 Simple Kubernetes Setup for V1

## Best Option: Play with Kubernetes (PWK) - FREE & EASY

**Why PWK?**
- ✅ **100% FREE** - No credit card needed
- ✅ **No installation** - Works in browser
- ✅ **4-hour sessions** - Perfect for testing/demos
- ✅ **Full K8s cluster** - Everything you need
- ✅ **Public access** - Can share Grafana dashboard URL

**URL:** https://labs.play-with-k8s.com/

---

## Quick Setup (5 minutes)

### Step 1: Get Kubernetes Cluster

1. Go to: https://labs.play-with-k8s.com/
2. Click **"Login"** (use GitHub account)
3. Click **"+ ADD NEW INSTANCE"** (creates a node)
4. Wait for node to be ready (green checkmark)

### Step 2: Install kubectl in Browser

In the terminal that opens, run:
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify
kubectl version --client
```

### Step 3: Initialize Kubernetes

```bash
# Initialize cluster (run on node 1)
kubeadm init --apiserver-advertise-address $(hostname -i) --pod-network-cidr 10.5.0.0/16

# Setup kubeconfig
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install network plugin
kubectl apply -f https://raw.githubusercontent.com/cloudnativelabs/kube-router/master/daemonset/kubeadm-kuberouter.yaml
```

### Step 4: Copy Your Files

**Option A: Clone from GitHub (Recommended)**
```bash
git clone https://github.com/suryamr2002/Fraud-detection-MLops-with-CI-CD-integration.git
cd Fraud-detection-MLops-with-CI-CD-integration
```

**Option B: Upload Files**
- Use the upload button in PWK interface
- Upload your `k8s/` folder

---

## Step 5: Deploy Everything

### Deploy Monitoring Stack

```bash
# Create namespace
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

### Deploy Fraud Detection API

```bash
# Deploy API
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Deploy HPA
kubectl apply -f k8s/hpa.yaml
```

### Verify

```bash
# Check everything is running
kubectl get pods --all-namespaces

# Check services
kubectl get svc --all-namespaces
```

---

## Step 6: Access Grafana Dashboard (UI)

### Get Public URL

PWK provides a public URL for services. To access Grafana:

**Option 1: Port Forward (Simple)**
```bash
# In PWK terminal, run:
kubectl port-forward -n monitoring svc/grafana-service 3000:3000
```

Then click the **"3000"** link that appears above the terminal - this opens Grafana in your browser!

**Option 2: Use NodePort (Public URL)**
The Grafana service is already configured as NodePort. PWK shows you the public IP.

1. Get node IP: Look at the top of your PWK instance (shows IP like `192.168.x.x`)
2. Access Grafana: `http://<node-ip>:30030`
3. Login: `admin` / `admin`

---

## Step 7: Test with Load

### Run Load Test

```bash
# Install Python dependencies (if needed)
pip install aiohttp requests

# Run load test (adjust URL to your API)
python load_test.py --url http://<node-ip>:<api-port> --duration 300 --rate 50
```

### Watch Auto-Scaling

```bash
# Terminal 1: Watch pods
watch kubectl get pods

# Terminal 2: Watch HPA
watch kubectl get hpa

# Terminal 3: Run load test
python load_test.py --url http://<node-ip>:<api-port> --duration 300 --rate 100
```

### View in Grafana

1. Open Grafana dashboard (from Step 6)
2. Go to **"Fraud Detection API - Real-Time Monitoring"** dashboard
3. Watch:
   - **Requests/sec** increasing
   - **Pod Count** scaling up (2 → 10)
   - **P95 Latency** (should stay stable)
   - **CPU/Memory** usage

---

## 📸 Screenshots for Resume

Capture:
1. ✅ Grafana dashboard showing metrics
2. ✅ `kubectl get pods` showing multiple pods (scaled up)
3. ✅ `kubectl get hpa` showing current/target replicas
4. ✅ Load test results
5. ✅ GitHub Actions workflow success

---

## 🔄 Alternative: DigitalOcean ($12/month)

If you want a more permanent solution:

1. **Sign up**: https://www.digitalocean.com/
2. **Create K8s cluster**: Dashboard → Kubernetes → Create Cluster
3. **Download kubeconfig**: Dashboard → Download Config
4. **Save to**: `C:\Users\<username>\.kube\config` (Windows)
5. **Deploy**: Same commands as above

**Advantages:**
- ✅ More stable (doesn't expire)
- ✅ Better for demos/interviews
- ✅ Can keep running for weeks

---

## 🎯 Summary

**For V1 (Simple & Free):**
1. ✅ Use **Play with Kubernetes** (PWK)
2. ✅ Deploy everything (5 minutes)
3. ✅ Access Grafana via port-forward or NodePort
4. ✅ Run load test
5. ✅ Watch auto-scaling in Grafana UI
6. ✅ Screenshot everything

**Next Steps:**
1. Push code to GitHub (builds Docker image)
2. Go to PWK and deploy
3. Test and screenshot

---

**Questions?** Let me know if you need help with any step!

