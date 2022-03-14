#!/bin/bash
celery worker -E -B --autoscale=20,15 --loglevel=INFO -Ofair --app=config.celery:app
