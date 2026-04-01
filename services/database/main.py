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
