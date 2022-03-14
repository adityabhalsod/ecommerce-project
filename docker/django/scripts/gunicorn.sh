#!/bin/bash
gunicorn --log-level debug --bind 0.0.0.0:80 --graceful-timeout 180000 --timeout 180000 --worker-class sync --max-requests 500 --max-requests-jitter 25 --workers 10 --preload  config.wsgi
