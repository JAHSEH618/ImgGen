# Gunicorn configuration file for File Storage Service
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:10086"
backlog = 2048

# Worker processes - Using single worker to avoid session lock issues
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 60  # File upload timeout
keepalive = 2

# Restart workers after this many requests
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'file_storage_api'

# Server mechanics
daemon = False
pidfile = '/tmp/file_storage.pid'
user = None
group = None
tmp_upload_dir = None

# Environment
raw_env = [
    'FLASK_ENV=production',
]

# Preload app for better performance
preload_app = True

# Worker timeout
graceful_timeout = 30