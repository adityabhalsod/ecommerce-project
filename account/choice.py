from django.contrib.gis.db import models


class SystemDefaultGroup(models.TextChoices):
    ADMINISTRATION = "Administration"
    STORE_MANAGER = "Store Manager"
    DELIVERY_BOY = "Delivery Boy"
    PACKAGING_STAFF = "Packaging staff"
    CUSTOMER = "Customer"


class RetryType(models.TextChoices):
    TEXT = "text", "Text"
    VOICE = "voice", "Voice"


class AddressType(models.TextChoices):
    OFFICE = "office", "Office"
    HOME = "home", "Home"


EXCLUDE_GROUP = [
    SystemDefaultGroup.ADMINISTRATION,
    SystemDefaultGroup.STORE_MANAGER,
]
