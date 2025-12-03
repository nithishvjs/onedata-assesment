from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Counter, Gauge, Histogram, generate_latest
import time
import random

# --- Prometheus Instrumentation Setup ---

# 1. Counter: Tracks the total number of requests
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

# 2. Gauge: Tracks the number of currently active processes/requests
IN_FLIGHT_REQUESTS = Gauge(
    'http_requests_in_flight',
    'Current number of requests being processed'
)

# 3. Histogram: Tracks request duration and buckets the observations
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency distribution',
    ['endpoint']
)

app = Flask(__name__)
# The Prometheus client library automatically exports Flask metrics to /metrics
# using the DispatcherMiddleware. We just need to register our custom endpoint.

# --- Application Logic ---

@app.route('/')
def home():
    """A simple endpoint that also generates a random metric update."""
    start_time = time.time()
    
    # Increment the in-flight gauge
    IN_FLIGHT_REQUESTS.inc() 

    # Simulate work and random latency
    latency = random.uniform(0.01, 0.5)
    time.sleep(latency)
    
    # Decrement the in-flight gauge
    IN_FLIGHT_REQUESTS.dec()

    # Record metrics
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('/').observe(time.time() - start_time)

    return jsonify({"message": "Hello from the monitored application! Load time: {:.4f}s".format(latency)})


@app.route('/metrics')
def metrics():
    """Exposes Prometheus metrics endpoint."""
    # We use the Prometheus client library to generate the latest metrics format
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

# Use gunicorn to run this app, as defined in Dockerfile
if __name__ == '__main__':
    # This block is mainly for local debugging if not using gunicorn
    print("Starting Flask app on port 5000...")
    app.run(host='0.0.0.0', port=5000)
