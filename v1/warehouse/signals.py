from django.db.models.signals import post_save
from django.dispatch import receiver
from v1.warehouse.models import Purchase, StockTransfer
from v1.warehouse.tasks import stock_purchase, stock_transfer


@receiver(post_save, sender=Purchase)
def stock_purchase_signals(sender, instance, created, **kwargs):
    if instance:
        stock_purchase.delay(instance)
    return instance


@receiver(post_save, sender=StockTransfer)
def stock_transfer_signals(sender, instance, created, **kwargs):
    if instance:
        stock_transfer.delay(instance)
    return instance
