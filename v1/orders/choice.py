from django.contrib.gis.db import models
from base.utils import next_couple_of_min_time


def order_expired():
    return next_couple_of_min_time(30)


class OrderType(models.TextChoices):
    CASH_ON_DELIVERY = "cash_on_delivery", "Cash on delivery"
    ONLINE = "online", "Online"
    NOT_ATTEMPT = "not_attempt", "Not attempt"


class OrderStatus(models.TextChoices):
    ORDER_AWAITING_FOR_PAYMENT = (
        "order_awaiting_for_payment",
        "Order awaiting for payment",
    )
    ORDER_PLACED = "order_placed", "Order Placed"
    ORDER_PACKING_STARTING = "order_packing_starting", "Order packing starting"
    ORDER_PACKING_COMPLETED = "order_packing_completed", "Order packing completed"
    ORDER_PICKUP = "order_pickup", "Order pickup"
    ORDER_ON_THE_WAY = "order_on_the_way", "Order on the way"
    ORDER_DELIVERED = "order_delivery", "Order delivered"
    ORDER_CANCEL = "order_cancel", "Order cancel"
    ORDER_FAILED = "order_failed", "Order failed"
    NOT_ATTEMPT = "not_attempt", "Not attempt"


class RefundStatus(models.TextChoices):
    SUCCESSFUL = "successful", "Successful"
    FAILED = "failed", "Failed"
    IN_PROGRESS = "in_progress", "In progress"
    NOT_ATTEMPT = "not_attempt", "Not attempt"


class PaymentStatus(models.TextChoices):
    WATING = "wating", "Wating"
    SUCCESSFUL = "successful", "Successful"
    FAILED = "failed", "Failed"
