from django.contrib.gis.db import models


class ProductType(models.TextChoices):
    SINGLE = "single", "Single"
    VARIATION = "variation", "Variation"


class ProductTaxType(models.TextChoices):
    NOT_ATTEMPT = 0, "Not attempt"
    GST_5_PERCENTAGE = 5, "GST 5%"
    GST_12_PERCENTAGE = 12, "GST 12%"
    GST_14_PERCENTAGE = 14, "GST 14%"
    GST_18_PERCENTAGE = 18, "GST 18%"
    GST_28_PERCENTAGE = 28, "GST 28%"
