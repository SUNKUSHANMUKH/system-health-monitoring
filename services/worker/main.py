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
