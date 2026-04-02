# 🖥️ System Health Monitor

> A production-grade infrastructure monitoring platform built with Prometheus, Grafana, Jenkins CI/CD, and Kubernetes — designed for deep hands-on learning of observability and automation.

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 📖 Table of Contents

- [What This Project Does](#-what-this-project-does)
- [Architecture](#-architecture)
- [What You Will Learn](#-what-you-will-learn)
- [Prerequisites](#-prerequisites)
- [Phase 1 — Build the Monitor App](#-phase-1--build-the-monitor-app)
- [Phase 2 — Kubernetes Deployment](#-phase-2--kubernetes-deployment)
- [Phase 3 — Prometheus Deep Dive](#-phase-3--prometheus-deep-dive)
- [Phase 4 — Grafana Dashboard Mastery](#-phase-4--grafana-dashboard-mastery)
- [Phase 5 — Alerting with Alertmanager](#-phase-5--alerting-with-alertmanager)
- [Phase 6 — Jenkins CI/CD Deep Dive](#-phase-6--jenkins-cicd-deep-dive)
- [PromQL Query Reference](#-promql-query-reference)
- [Grafana Panel Reference](#-grafana-panel-reference)
- [Common Errors and Fixes](#-common-errors-and-fixes)
- [Project Structure](#-project-structure)

---

## 🎯 What This Project Does

This project monitors the health of a multi-service system in real time:

```
3 Services Running Simultaneously:
  ├── API Service      → handles HTTP requests
  ├── Worker Service   → processes background jobs
  └── Database Service → simulates DB queries

Each service reports:
  ├── CPU usage
  ├── Memory consumption
  ├── Request rates and error rates
  ├── Response time percentiles (p50, p95, p99)
  └── Service uptime

Prometheus scrapes all services every 15 seconds.
Grafana shows live dashboards with colour-coded alerts.
Alertmanager fires alerts when thresholds are crossed.
Jenkins auto-deploys every code change in under 2 minutes.
```

**Real-world analogy:** This is exactly what the DevOps team at any tech company uses to know if their systems are healthy — before users notice something is wrong.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Minikube (Kubernetes)                 │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ API Service │  │   Worker    │  │  Database Simulator │  │
│  │  :8001      │  │  Service    │  │      :8003          │  │
│  │  /metrics   │  │  :8002      │  │      /metrics       │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                    │              │
│         └────────────────┴────────────────────┘              │
│                          │                                   │
│                          ▼                                   │
│               ┌──────────────────┐                           │
│               │    Prometheus    │                           │
│               │  scrapes every   │                           │
│               │    15 seconds    │                           │
│               └────────┬─────────┘                           │
│                        │                                     │
│           ┌────────────┼────────────┐                        │
│           ▼            ▼            ▼                        │
│     ┌──────────┐ ┌──────────┐ ┌──────────────┐              │
│     │ Grafana  │ │  Alert   │ │   Grafana    │              │
│     │Dashboard │ │ manager  │ │   Alerts     │              │
│     └──────────┘ └──────────┘ └──────────────┘              │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                Jenkins CI/CD Pipeline                 │   │
│  │  GitHub Push → Test → Build → Deploy → Verify        │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎓 What You Will Learn

### Prometheus (Deep)
- Writing custom metrics: Counter, Gauge, Histogram, Summary
- Understanding labels and cardinality
- Writing PromQL queries from scratch
- Configuring scrape targets and intervals
- Setting up recording rules for performance
- Understanding the difference between push vs pull metrics

### Grafana (Deep)
- Building dashboards from zero — no templates
- Every panel type: Time series, Stat, Gauge, Heatmap, Table, Bar chart
- Setting thresholds and colour coding
- Creating variables for dynamic dashboards
- Setting up alert rules with conditions
- Linking panels together with drill-downs

### Jenkins (Deep)
- Multi-stage pipelines with real test reports
- Parallel stages for faster builds
- Environment-specific deployments
- Automatic rollback on failure
- Build notifications
- Parameterised builds

### Kubernetes (Deeper)
- Liveness and readiness probes
- Resource requests and limits
- ConfigMaps and Secrets
- Horizontal Pod Autoscaler
- Namespaces for environment separation
- Annotations for Prometheus discovery

---

## ✅ Prerequisites

### Tools to Install

**Docker Desktop** — download from [docker.com](https://docker.com)
```bash
docker --version
# Expected: Docker version 24.x.x
```

**Minikube**
```bash
# macOS
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

minikube version
```

**kubectl**
```bash
brew install kubectl        # macOS
sudo apt install kubectl    # Linux

kubectl version --client
```

**Helm** (Kubernetes package manager)
```bash
brew install helm           # macOS
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash  # Linux

helm version
```

**Python 3.10+**
```bash
python3 --version
pip3 install fastapi uvicorn prometheus-client httpx pytest
```

---

## 🚀 Phase 1 — Build the Monitor App

### Step 1.1 — Create Project Structure

```bash
mkdir system-health-monitor && cd system-health-monitor
mkdir -p services/api services/worker services/database
mkdir -p k8s monitoring jenkins tests
```

### Step 1.2 — API Service (with custom metrics)

```bash
cat > services/api/main.py << 'EOF'
from fastapi import FastAPI, Request
from prometheus_client import (
    Counter, Gauge, Histogram,
    generate_latest, CONTENT_TYPE_LATEST
)
from starlette.responses import Response
import time, random, threading

app = FastAPI(title="API Service")

# ── COUNTERS (only go up) ─────────────────────────────────────
http_requests_total = Counter(
    'api_http_requests_total',
    'Total HTTP requests received',
    ['method', 'endpoint', 'status_code']
)

errors_total = Counter(
    'api_errors_total',
    'Total errors encountered',
    ['error_type']
)

# ── GAUGES (go up and down) ───────────────────────────────────
active_connections = Gauge(
    'api_active_connections',
    'Number of active connections right now'
)

cpu_usage_percent = Gauge(
    'api_cpu_usage_percent',
    'Simulated CPU usage percentage'
)

memory_usage_percent = Gauge(
    'api_memory_usage_percent',
    'Simulated memory usage percentage'
)

# ── HISTOGRAM (measures distributions) ───────────────────────
request_duration_seconds = Histogram(
    'api_request_duration_seconds',
    'HTTP request duration in seconds',
    ['endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)

# ── BACKGROUND: simulate realistic system behaviour ──────────
def simulate_system():
    while True:
        cpu_usage_percent.set(random.uniform(20, 85))
        memory_usage_percent.set(random.uniform(40, 75))
        active_connections.set(random.randint(5, 200))
        time.sleep(3)

threading.Thread(target=simulate_system, daemon=True).start()

# ── MIDDLEWARE: auto-track every request ─────────────────────
@app.middleware("http")
async def track_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    if request.url.path != "/metrics":
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        request_duration_seconds.labels(
            endpoint=request.url.path
        ).observe(duration)
    return response

# ── ENDPOINTS ────────────────────────────────────────────────
@app.get("/")
def health():
    return {"service": "api", "status": "healthy"}

@app.get("/users")
def get_users():
    if random.random() < 0.05:
        errors_total.labels(error_type="db_timeout").inc()
        return {"error": "Database timeout"}, 500
    time.sleep(random.uniform(0.01, 0.3))
    return {"users": random.randint(100, 9999)}

@app.get("/search")
def search():
    time.sleep(random.uniform(0.05, 0.8))
    return {"results": random.randint(0, 50)}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
EOF
```

### Step 1.3 — Worker Service

```bash
cat > services/worker/main.py << 'EOF'
from fastapi import FastAPI
from prometheus_client import (
    Counter, Gauge, Histogram,
    generate_latest, CONTENT_TYPE_LATEST
)
from starlette.responses import Response
import time, random, threading

app = FastAPI(title="Worker Service")

jobs_processed = Counter(
    'worker_jobs_processed_total',
    'Total background jobs processed',
    ['job_type', 'status']
)

queue_depth = Gauge(
    'worker_queue_depth',
    'Number of jobs waiting in queue'
)

job_duration = Histogram(
    'worker_job_duration_seconds',
    'Time taken to process a job',
    ['job_type'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

worker_memory = Gauge('worker_memory_usage_percent', 'Worker memory usage')
worker_cpu    = Gauge('worker_cpu_usage_percent',    'Worker CPU usage')

def run_jobs():
    job_types = ['email', 'report', 'cleanup', 'sync']
    while True:
        queue_depth.set(random.randint(0, 150))
        worker_memory.set(random.uniform(30, 70))
        worker_cpu.set(random.uniform(10, 60))
        job = random.choice(job_types)
        duration = random.uniform(0.1, 8.0)
        time.sleep(duration)
        status = 'success' if random.random() > 0.08 else 'failed'
        jobs_processed.labels(job_type=job, status=status).inc()
        job_duration.labels(job_type=job).observe(duration)

threading.Thread(target=run_jobs, daemon=True).start()

@app.get("/")
def health():
    return {"service": "worker", "status": "healthy"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
EOF
```

### Step 1.4 — Database Service

```bash
cat > services/database/main.py << 'EOF'
from fastapi import FastAPI
from prometheus_client import (
    Counter, Gauge, Histogram,
    generate_latest, CONTENT_TYPE_LATEST
)
from starlette.responses import Response
import time, random, threading

app = FastAPI(title="Database Service")

db_queries_total   = Counter('db_queries_total',   'Total DB queries', ['operation', 'status'])
db_connections     = Gauge('db_connections_active', 'Active DB connections')
db_pool_size       = Gauge('db_connection_pool_size','Total connection pool size')
db_query_duration  = Histogram('db_query_duration_seconds', 'Query duration',
                               ['operation'], buckets=[0.001,0.005,0.01,0.05,0.1,0.5,1.0])
db_memory          = Gauge('db_memory_usage_percent', 'DB memory usage')
db_disk_usage      = Gauge('db_disk_usage_percent',   'DB disk usage percent')
db_replication_lag = Gauge('db_replication_lag_seconds', 'Replication lag')

def simulate_db():
    db_pool_size.set(100)
    ops = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
    while True:
        db_connections.set(random.randint(10, 95))
        db_memory.set(random.uniform(45, 80))
        db_disk_usage.set(random.uniform(30, 65))
        db_replication_lag.set(random.uniform(0, 0.5))
        op = random.choice(ops)
        dur = random.uniform(0.001, 0.8)
        time.sleep(max(0.1, dur))
        status = 'success' if random.random() > 0.02 else 'error'
        db_queries_total.labels(operation=op, status=status).inc()
        db_query_duration.labels(operation=op).observe(dur)

threading.Thread(target=simulate_db, daemon=True).start()

@app.get("/")
def health():
    return {"service": "database", "status": "healthy"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
EOF
```

### Step 1.5 — Shared requirements.txt and Dockerfile

```bash
cat > requirements.txt << 'EOF'
fastapi
uvicorn
prometheus-client
httpx
pytest
EOF

# One Dockerfile works for all 3 services
# We pass the service path as a build argument
cat > dockerfile << 'EOF'
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG SERVICE=api
CMD ["sh", "-c", "uvicorn services.${SERVICE}.main:app --host 0.0.0.0 --port 8000"]
EOF
```

### Step 1.6 — Build and Test All 3 Services

```bash
# Test each service locally one at a time
docker build -t health-api:v1 --build-arg SERVICE=api .
docker run --rm -p 8001:8000 health-api:v1
```

In a new terminal:
```bash
curl http://localhost:8001/
curl http://localhost:8001/users
curl http://localhost:8001/metrics
```

The `/metrics` output will show your raw Prometheus data:
```
# HELP api_http_requests_total Total HTTP requests received
api_http_requests_total{endpoint="/users",method="GET",status_code="200"} 3.0
api_cpu_usage_percent 67.4
api_memory_usage_percent 52.1
```

> ✅ **Checkpoint:** You can see metrics in the terminal. This is exactly what Prometheus will scrape automatically.

---

## ☸️ Phase 2 — Kubernetes Deployment

### Step 2.1 — Start Minikube and Build Images

```bash
minikube start --driver=docker

# CRITICAL: build inside Minikube's Docker
eval $(minikube docker-env)

docker build -t health-api:v1      --build-arg SERVICE=api      .
docker build -t health-worker:v1   --build-arg SERVICE=worker   .
docker build -t health-database:v1 --build-arg SERVICE=database .

# Verify all 3 images are available
minikube image ls | grep health
```

### Step 2.2 — Create Kubernetes Manifests

```bash
cat > k8s/services.yaml << 'EOF'
# ── API SERVICE ───────────────────────────────────────────────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: health-api
  template:
    metadata:
      labels:
        app: health-api
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port:   "8000"
        prometheus.io/path:   "/metrics"
    spec:
      containers:
      - name: health-api
        image: health-api:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 15
        readinessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: health-api-svc
spec:
  selector:
    app: health-api
  ports:
  - port: 80
    targetPort: 8000
  type: NodePort
---
# ── WORKER SERVICE ────────────────────────────────────────────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-worker
spec:
  replicas: 1
  selector:
    matchLabels:
      app: health-worker
  template:
    metadata:
      labels:
        app: health-worker
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port:   "8000"
        prometheus.io/path:   "/metrics"
    spec:
      containers:
      - name: health-worker
        image: health-worker:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 15
---
apiVersion: v1
kind: Service
metadata:
  name: health-worker-svc
spec:
  selector:
    app: health-worker
  ports:
  - port: 80
    targetPort: 8000
  type: NodePort
---
# ── DATABASE SERVICE ──────────────────────────────────────────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-database
spec:
  replicas: 1
  selector:
    matchLabels:
      app: health-database
  template:
    metadata:
      labels:
        app: health-database
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port:   "8000"
        prometheus.io/path:   "/metrics"
    spec:
      containers:
      - name: health-database
        image: health-database:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "300m"
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 15
---
apiVersion: v1
kind: Service
metadata:
  name: health-database-svc
spec:
  selector:
    app: health-database
  ports:
  - port: 80
    targetPort: 8000
  type: NodePort
EOF
```

### Step 2.3 — Deploy Everything

```bash
kubectl apply -f k8s/services.yaml
kubectl get pods -w
```

Expected — all 4 pods running:
```
NAME                               READY   STATUS    RESTARTS   AGE
health-api-xxxxxxxxx-xxxxx         1/1     Running   0          30s
health-api-xxxxxxxxx-xxxxx         1/1     Running   0          30s
health-worker-xxxxxxxxx-xxxxx      1/1     Running   0          30s
health-database-xxxxxxxxx-xxxxx    1/1     Running   0          30s
```

---

## 📈 Phase 3 — Prometheus Deep Dive

### Step 3.1 — Install Prometheus

```bash
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=admin123 \
  --set prometheus.prometheusSpec.scrapeInterval=15s

kubectl get pods -n monitoring -w
# Wait until all show Running — takes 2 to 3 minutes
```

### Step 3.2 — Access Prometheus UI

```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus \
  9090:9090 -n monitoring
```

Open [http://localhost:9090](http://localhost:9090)

### Step 3.3 — Learn PromQL — Start Simple and Build Up

Go to Prometheus UI → click **Graph** tab and run each query:

**Level 1 — Raw metrics (just look at data)**
```promql
api_http_requests_total
api_cpu_usage_percent
worker_queue_depth
db_connections_active
```

**Level 2 — Rates (how fast things are changing per second)**
```promql
rate(api_http_requests_total[5m])
rate(db_queries_total[5m])
rate(worker_jobs_processed_total[5m])
```

**Level 3 — Aggregations (sum across all pods)**
```promql
sum(rate(api_http_requests_total[5m]))
sum(rate(api_http_requests_total[5m])) by (status_code)
sum(rate(db_queries_total[5m])) by (operation)
```

**Level 4 — Error rates (the most important production query)**
```promql
# API error rate as a percentage
sum(rate(api_http_requests_total{status_code=~"5.."}[5m]))
/
sum(rate(api_http_requests_total[5m])) * 100

# Worker job failure rate
sum(rate(worker_jobs_processed_total{status="failed"}[5m]))
/
sum(rate(worker_jobs_processed_total[5m])) * 100
```

**Level 5 — Percentiles (response time p50 p95 p99)**
```promql
# 50th percentile (median) response time
histogram_quantile(0.50, rate(api_request_duration_seconds_bucket[5m]))

# 95th percentile (what 95% of users experience)
histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))

# 99th percentile (worst 1% of users)
histogram_quantile(0.99, rate(api_request_duration_seconds_bucket[5m]))
```

> 💡 **p95 and p99 are the most important metrics in any production system.** Average response time hides problems — percentiles reveal them.

---

## 📊 Phase 4 — Grafana Dashboard Mastery

### Step 4.1 — Access Grafana

```bash
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
```

Open [http://localhost:3000](http://localhost:3000) — login: `admin` / `admin123`

### Step 4.2 — Create Your Dashboard from Scratch

1. Click **+** (left sidebar) → **New Dashboard**
2. Click **Add visualization**
3. Set data source to **Prometheus**

Build these 6 panels one by one:

---

**Panel 1 — Request Rate (Time Series)**

Query:
```promql
sum(rate(api_http_requests_total[5m])) by (endpoint)
```
- Visualization: **Time series**
- Title: `API Request Rate by Endpoint`
- Legend: `{{endpoint}}`
- Unit: `requests/sec`

---

**Panel 2 — Error Rate % (Stat panel with colour)**

Query:
```promql
sum(rate(api_http_requests_total{status_code=~"5.."}[5m]))
/
sum(rate(api_http_requests_total[5m])) * 100
```
- Visualization: **Stat**
- Title: `API Error Rate`
- Unit: `Percent (0-100)`
- Thresholds:
  - Green: 0
  - Yellow: 1
  - Red: 5

---

**Panel 3 — Response Time Percentiles (Time Series)**

Add 3 queries (A, B, C):
```promql
# Query A — label: p50
histogram_quantile(0.50, rate(api_request_duration_seconds_bucket[5m]))

# Query B — label: p95
histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))

# Query C — label: p99
histogram_quantile(0.99, rate(api_request_duration_seconds_bucket[5m]))
```
- Visualization: **Time series**
- Title: `Response Time Percentiles`
- Unit: `seconds`

---

**Panel 4 — CPU and Memory (Gauge)**

```promql
avg(api_cpu_usage_percent)
```
- Visualization: **Gauge**
- Title: `API CPU Usage`
- Min: 0, Max: 100
- Thresholds: Green 0 → Yellow 70 → Red 85

---

**Panel 5 — Worker Queue Depth (Time Series)**

```promql
worker_queue_depth
```
- Visualization: **Time series**
- Title: `Worker Queue Depth`
- Add threshold line at 100 (right panel → Thresholds)

---

**Panel 6 — Database Connections (Bar gauge)**

```promql
db_connections_active
```
- Visualization: **Bar gauge**
- Title: `Active DB Connections`
- Max: 100
- Thresholds: Green 0 → Yellow 70 → Red 90

---

### Step 4.3 — Add a Dashboard Variable (makes it dynamic)

1. Click the **gear icon** (Dashboard settings) → **Variables** → **Add variable**
2. Name: `service`
3. Type: **Query**
4. Query: `label_values(up, job)`
5. Now use `$service` in your panel queries to filter by service

### Step 4.4 — Save Your Dashboard

1. Click **Save** (floppy disk icon top right)
2. Name: `System Health Monitor`
3. Click **Save**

---

## 🚨 Phase 5 — Alerting with Alertmanager

### Step 5.1 — Create Alert Rules

```bash
cat > monitoring/alerts.yaml << 'EOF'
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: health-monitor-alerts
  namespace: monitoring
  labels:
    release: prometheus
spec:
  groups:
  - name: system.health
    rules:

    # Alert when API error rate exceeds 5%
    - alert: HighAPIErrorRate
      expr: |
        sum(rate(api_http_requests_total{status_code=~"5.."}[5m]))
        /
        sum(rate(api_http_requests_total[5m])) * 100 > 5
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "High API error rate detected"
        description: "API error rate is {{ $value | printf \"%.1f\" }}%"

    # Alert when CPU stays above 80% for 5 minutes
    - alert: HighCPUUsage
      expr: avg(api_cpu_usage_percent) > 80
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High CPU usage on API service"
        description: "CPU at {{ $value | printf \"%.1f\" }}%"

    # Alert when worker queue gets too deep
    - alert: WorkerQueueBacklog
      expr: worker_queue_depth > 100
      for: 3m
      labels:
        severity: warning
      annotations:
        summary: "Worker queue is backing up"
        description: "Queue depth is {{ $value }} jobs"

    # Alert when DB connections near limit
    - alert: DatabaseConnectionsHigh
      expr: db_connections_active > 85
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "Database connections near limit"
        description: "Active connections: {{ $value }}/100"
EOF

kubectl apply -f monitoring/alerts.yaml
```

### Step 5.2 — View Alerts in Prometheus and Grafana

In Prometheus UI ([http://localhost:9090](http://localhost:9090)):
- Click **Alerts** tab — see your alert rules and which are firing

In Grafana ([http://localhost:3000](http://localhost:3000)):
- Click **Alerting** (bell icon) → **Alert Rules**
- You can also create Grafana-native alerts from any panel

---

## 🔧 Phase 6 — Jenkins CI/CD Deep Dive

### Step 6.1 — Start Jenkins

```bash
docker run -d \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins \
  jenkins/jenkins:lts

# Get password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open [http://localhost:8080](http://localhost:8080) — install suggested plugins.

### Step 6.2 — Write a Production-Grade Jenkinsfile

```bash
cat > Jenkinsfile << 'EOF'
pipeline {
    agent any

    environment {
        APP_VERSION = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Building version ${APP_VERSION}"
                checkout scm
            }
        }

        // Run tests for all 3 services at the same time
        stage('Test All Services') {
            parallel {
                stage('Test API') {
                    steps {
                        sh 'pip install pytest httpx fastapi prometheus-client uvicorn'
                        sh 'pytest tests/test_api.py -v'
                    }
                }
                stage('Test Worker') {
                    steps {
                        sh 'pytest tests/test_worker.py -v'
                    }
                }
                stage('Test Database') {
                    steps {
                        sh 'pytest tests/test_database.py -v'
                    }
                }
            }
        }

        // Build all 3 Docker images at the same time
        stage('Build Images') {
            parallel {
                stage('Build API') {
                    steps {
                        sh "docker build --build-arg SERVICE=api -t health-api:${APP_VERSION} ."
                    }
                }
                stage('Build Worker') {
                    steps {
                        sh "docker build --build-arg SERVICE=worker -t health-worker:${APP_VERSION} ."
                    }
                }
                stage('Build Database') {
                    steps {
                        sh "docker build --build-arg SERVICE=database -t health-database:${APP_VERSION} ."
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl set image deployment/health-api health-api=health-api:${APP_VERSION}"
                sh "kubectl set image deployment/health-worker health-worker=health-worker:${APP_VERSION}"
                sh "kubectl set image deployment/health-database health-database=health-database:${APP_VERSION}"
                sh "kubectl rollout status deployment/health-api --timeout=120s"
                sh "kubectl rollout status deployment/health-worker --timeout=120s"
                sh "kubectl rollout status deployment/health-database --timeout=120s"
            }
        }

        stage('Verify Health') {
            steps {
                sh 'kubectl get pods -l app=health-api'
                sh 'kubectl get pods -l app=health-worker'
                sh 'kubectl get pods -l app=health-database'
                echo "All services deployed as ${APP_VERSION}"
            }
        }
    }

    post {
        success {
            echo "Deployment ${APP_VERSION} succeeded"
        }
        failure {
            echo "Deployment failed — rolling back all services"
            sh 'kubectl rollout undo deployment/health-api'
            sh 'kubectl rollout undo deployment/health-worker'
            sh 'kubectl rollout undo deployment/health-database'
        }
    }
}
EOF
```

> 💡 **Key learning:** `parallel` stages run at the same time — your 3 services test and build simultaneously, cutting pipeline time by 3x.

### Step 6.3 — Write Tests for Jenkins to Run

```bash
cat > tests/test_api.py << 'EOF'
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.api.main import app

client = TestClient(app)

def test_health_check():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "api"

def test_users_endpoint():
    r = client.get("/users")
    assert r.status_code in [200, 500]

def test_metrics_exposed():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"api_http_requests_total" in r.content
    assert b"api_cpu_usage_percent" in r.content
EOF

cat > tests/test_worker.py << 'EOF'
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.worker.main import app

client = TestClient(app)

def test_health_check():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "worker"

def test_metrics_exposed():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"worker_jobs_processed_total" in r.content
EOF

cat > tests/test_database.py << 'EOF'
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.database.main import app

client = TestClient(app)

def test_health_check():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "database"

def test_metrics_exposed():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"db_queries_total" in r.content
    assert b"db_connections_active" in r.content
EOF
```

---

## 📐 PromQL Query Reference

| What You Want to Know | PromQL Query |
|---|---|
| Total requests per second | `sum(rate(api_http_requests_total[5m]))` |
| Error rate percentage | `sum(rate(api_http_requests_total{status_code=~"5.."}[5m])) / sum(rate(api_http_requests_total[5m])) * 100` |
| Median response time | `histogram_quantile(0.50, rate(api_request_duration_seconds_bucket[5m]))` |
| p95 response time | `histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))` |
| p99 response time | `histogram_quantile(0.99, rate(api_request_duration_seconds_bucket[5m]))` |
| Average CPU across all pods | `avg(api_cpu_usage_percent)` |
| Worker job failure rate | `sum(rate(worker_jobs_processed_total{status="failed"}[5m])) / sum(rate(worker_jobs_processed_total[5m])) * 100` |
| DB queries per second | `sum(rate(db_queries_total[5m])) by (operation)` |
| Active DB connections | `db_connections_active` |
| Queue depth over time | `worker_queue_depth` |

---

## 🖥️ Grafana Panel Reference

| Panel Type | Best Used For | Example |
|---|---|---|
| **Time series** | Anything over time | Request rate, CPU over 24h |
| **Stat** | Single current value | Error rate right now |
| **Gauge** | Value with min/max context | CPU %, memory % |
| **Bar gauge** | Comparing across services | Connections per service |
| **Heatmap** | Distribution over time | Response time distribution |
| **Table** | Multiple values at once | All services status |
| **Alert list** | Active alerts summary | What is firing now |

---

## 🐛 Common Errors and Fixes

### Prometheus not scraping your service
```bash
# Check targets in Prometheus UI
# Go to http://localhost:9090 → Status → Targets
# Your service should appear here

# If missing — check the annotations in your deployment YAML:
kubectl describe pod health-api-xxxxx | grep annotations -A 5
# Should show: prometheus.io/scrape: "true"
```

### Grafana shows "No data"
```bash
# 1. Check data source is connected
# Grafana → Configuration → Data Sources → Prometheus → Test

# 2. Verify the metric name exists in Prometheus first
# Go to Prometheus UI and run the query there first
# If it works in Prometheus but not Grafana, check the data source URL

# 3. Check time range in Grafana — set to Last 15 minutes
```

### Alert rule not firing
```bash
# Check rule was applied
kubectl get prometheusrule -n monitoring

# Check Prometheus loaded it
# Go to http://localhost:9090 → Status → Rules
# Your alert name should appear

# If missing — check the label on the PrometheusRule matches:
kubectl get prometheusrule health-monitor-alerts -n monitoring -o yaml | grep labels -A 3
# Must have: release: prometheus
```

### Jenkins parallel stage fails
```bash
# Each parallel branch runs independently
# If one branch fails, others continue
# Check which branch failed in the Jenkins console output
# Blue Ocean view (Jenkins → Open Blue Ocean) shows parallel stages visually
```

### Pod stuck in Pending
```bash
kubectl describe pod <pod-name> | grep -A 10 Events
# Usually means: not enough memory or CPU on the node
# Fix: reduce resource requests in deployment YAML
#   requests:
#     memory: "32Mi"   (reduce from 64Mi)
#     cpu: "25m"       (reduce from 50m)
```

---

## 📁 Project Structure

```
system-health-monitor/
├── services/
│   ├── api/
│   │   └── main.py          # API service with custom metrics
│   ├── worker/
│   │   └── main.py          # Worker service with job metrics
│   └── database/
│       └── main.py          # DB service with query metrics
├── k8s/
│   └── services.yaml        # All 3 deployments + services
├── monitoring/
│   └── alerts.yaml          # Prometheus alert rules
├── jenkins/
│   └── Jenkinsfile          # CI/CD pipeline
├── tests/
│   ├── test_api.py
│   ├── test_worker.py
│   └── test_database.py
├── dockerfile               # Single dockerfile for all services
├── requirements.txt
└── README.md
```

---

## 🆚 What This Teaches vs Project 1

| Skill | Project 1 | Project 2 (this one) |
|---|---|---|
| Prometheus | Installed only | Custom counters, gauges, histograms, alerts |
| Grafana | Installed only | 6 panel types, variables, alert rules |
| Jenkins | Single stage | Parallel stages, test reports, rollback |
| Kubernetes | Basic pods | Probes, resource limits, namespaces |
| Python | One service | Three services with background threads |
| PromQL | Never used | 10+ real production queries |
| Alerting | Never done | Full alert rule lifecycle |

---

## 📚 Resources for Going Deeper

- [Prometheus Docs — Writing Exporters](https://prometheus.io/docs/instrumenting/writing_exporters/)
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)
- [Grafana Alerting Docs](https://grafana.com/docs/grafana/latest/alerting/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

---

> *"Observability is not about collecting more data. It is about asking the right questions of your system."*

---

**Built as Project 2 of a DevOps + AI learning series.**
