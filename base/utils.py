from datetime import timedelta
from django.utils import timezone
from dateutil.tz import gettz


def next_couple_of_min_time(min=30):
    return timezone.now() + timedelta(minutes=min)


def next_couple_of_hour_time(hour=1):
    return timezone.now() + timedelta(hours=hour)


def get_iso8601_time(time):
    if not time:
        time = timezone.now()
    zone = "Asia/Kolkata"
    dt_zone = time.astimezone(gettz(zone))
    return dt_zone.isoformat(timespec="seconds")
