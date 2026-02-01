import os

# Use Render's PORT or default to 8000
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Worker configuration (1 worker for free tier)
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "fastapi_app"