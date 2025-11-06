import os
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"

# Logging
loglevel = os.environ.get("LOG_LEVEL", "info")
accesslog = "-"  # Log para stdout
errorlog = "-"   # Log para stderr

# Worker processes
workers = int(os.environ.get("NUM_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"  # Importante: usa Uvicorn como worker

# Requests
max_requests = int(os.environ.get("MAX_REQUESTS", 500))
max_requests_jitter = int(os.environ.get("MAX_REQUESTS_JITTER", 50))

# Timeouts
timeout = int(os.environ.get("TIMEOUT", 120))  # Maior para LLM
graceful_timeout = int(os.environ.get("GRACEFUL_TIMEOUT", 30))
keepalive = int(os.environ.get("KEEPALIVE", 5))

# Performance
preload_app = True  # Carrega app antes de fork (economiza memória)