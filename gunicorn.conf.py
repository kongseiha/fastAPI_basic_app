import os

port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 2

accesslog = "-"
errorlog = "-"
loglevel = "info"