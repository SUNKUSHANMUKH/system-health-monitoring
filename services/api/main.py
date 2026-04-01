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
