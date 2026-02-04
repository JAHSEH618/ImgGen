# Gunicorn configuration file
import os

# Server socket
bind = "0.0.0.0:8088"
backlog = 2048

# Worker processes - Using single worker to avoid session lock issues
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 5 minutes for AI processing
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'gemini_api'

# Server mechanics
daemon = False
pidfile = '/tmp/gemini_api.pid'
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment for HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Environment
raw_env = [
    'FLASK_ENV=production',
    'GEMINI_API_KEY=' + os.environ.get('GEMINI_API_KEY', ''),
]

# Preload app for better performance
preload_app = True

# Worker timeout for long-running AI requests
graceful_timeout = 60