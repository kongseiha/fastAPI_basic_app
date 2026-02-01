import multiprocessing

# Bind to all interfaces on port 8000 (Render sets PORT env variable)
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes (adjusted for Render free tier)
workers = 1  # Free tier only allows 1 worker
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120  # Increased timeout
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "fastapi_app"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Graceful shutdown
graceful_timeout = 120