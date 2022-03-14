import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set default Django settings module for celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("quickly")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings")

app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_TIMEZONE = "UTC"
app.conf.beat_schedule = {
    "set-automatically-deactivate-membership-crontab": {
        "task": "v1.membership.tasks.set_automatically_deactivate_membership",
        "schedule": crontab(hour="*/24"),  # Everydays
    },
    "automatically-order-expired": {
        "task": "v1.orders.tasks.automatically_order_expired",
        "schedule": crontab(minute="*/30"),  # Every 30m
    },
    "automatic-change-activity-after-expired-voucher": {
        "task": "v1.orders.promotion.automatic_change_activity_after_expired_voucher",
        "schedule": crontab(hour="*/24"),  # Everydays
    },
}

app.conf.task_routes = {}
app.conf.task_annotations = {}

app.conf.accept_content = settings.CELERY_ACCEPT_CONTENT
app.conf.task_serializer = settings.CELERY_TASK_SERIALIZER
app.conf.result_serializer = settings.CELERY_RESULT_SERIALIZER
app.conf.worker_prefetch_multiplier = settings.CELERY_WORKER_PREFETCH_MULTIPLIER
# To restart worker processes after every task
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.broker_transport_options = settings.BROKER_TRANSPORT_OPTIONS
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.autodiscover_tasks()
