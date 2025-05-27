# Gunicorn configuration file for Barlau.kz Django project

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/barlau/gunicorn_access.log"
errorlog = "/var/log/barlau/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "barlau_gunicorn"

# Server mechanics
daemon = False
pidfile = "/var/run/barlau/gunicorn.pid"
user = "barlau"
group = "barlau"
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Environment
raw_env = [
    "DJANGO_SETTINGS_MODULE=barlau.settings_production",
] 