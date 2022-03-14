from django.contrib.gis.db import models


class ValueType(models.TextChoices):
    FIXED = "fixed", "Fixed (Rs.)"
    PERCENTAGE = "percentage", "Percentage (%)"


class VoucherType(models.TextChoices):
    ENTIRE_ORDER = "entire_order", "Entire order"
    SPECIFIC_STORE = (
        "specific_store",
        "Specific Store",
    )
    SPECIFIC_PRODUCT = (
        "specific_product",
        "Specific products, collections and categories",
    )


class DiscountType(models.TextChoices):
    INSTANT_DISCOUNT = "instant_discount", "Instant Discount"
    CASHBACK_DISCOUNT = "cashback_discount", "Cashback Discount"
