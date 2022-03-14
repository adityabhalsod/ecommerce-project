from django.contrib.gis.db import models


class OrderType(models.TextChoices):
    CASH_ON_DELIVERY = "cash_on_delivery", "Cash on delivery"
    ONLINE = "online", "Online"
