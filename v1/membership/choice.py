from django.contrib.gis.db import models


class MembershipTypeChoices(models.TextChoices):
    ONE_MONTH = "one_month", "One month"
    THREE_MONTH = "three_month", "Three month"
    HALF_YEAR = "half_year", "Half year"
    ONE_YEAR = "one_year", "One year"
    NOT_ATTEMPT = "not_attempt", "Not attempt"
