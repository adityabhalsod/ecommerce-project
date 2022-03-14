from django.contrib.gis.db import models
from django.utils import timezone
from base.models import BaseModel
from v1.wallet.choice import (
    TransactionMethod,
    TransactionPlatform,
    TransactionStatus,
    TransactionType,
)
from django.db.models import Max

# TODO: Firebase notification
# TODO: SMS
# TODO: Email


class CustomerWallet(BaseModel):
    customer = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="customer_wallet",
    )
    balance_amount = models.FloatField(default=0.0, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = [("customer",)]

    def __str__(self):
        return str(self.pk)


class DeliveryBoyWallet(BaseModel):
    delivery_boy = models.ForeignKey(
        "delivery.DeliveryBoy",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_boy_wallet",
    )
    balance_amount = models.FloatField(default=0.0, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = [("delivery_boy",)]

    def __str__(self):
        return str(self.pk)


class Transaction(BaseModel):
    name = models.CharField(max_length=255, default="", null=True, blank=True)
    notes = models.TextField(default="", null=True, blank=True)
    reference = models.CharField(max_length=255, default="", null=True, blank=True)
    payment_payload = models.TextField(default="", null=True, blank=True)
    payment_response = models.TextField(default="", null=True, blank=True)
    transaction_type = models.CharField(
        max_length=255,
        choices=TransactionType.choices,
        default=TransactionType.NOT_ATTEMPT,
    )
    method = models.CharField(
        max_length=255,
        choices=TransactionMethod.choices,
        default=TransactionMethod.NOT_ATTEMPT,
    )
    status = models.CharField(
        max_length=255,
        choices=TransactionStatus.choices,
        default=TransactionStatus.NOT_ATTEMPT,
    )
    platform = models.CharField(
        max_length=255,
        choices=TransactionPlatform.choices,
        default=TransactionPlatform.NOT_ATTEMPT,
    )
    customer_wallet = models.ForeignKey(
        "wallet.CustomerWallet",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="customer_wallet_transaction",
    )
    delivery_boy_wallet = models.ForeignKey(
        "wallet.DeliveryBoyWallet",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_boy_wallet_transaction",
    )
    datetime = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(default=0.0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Current count
            current_count = (
                self.__class__.objects.aggregate(Max("id")).get("id__max") or 0
            )
            self.reference = "{}{:010d}".format(
                "TXT-", current_count + 1 if current_count is not None else 1
            )
        return super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)


class CaseOnDeliveryCollectionHistory(BaseModel):
    name = models.CharField(max_length=255, default="", null=True, blank=True)
    notes = models.TextField(default="", null=True, blank=True)
    reference = models.CharField(max_length=255, default="", null=True, blank=True)
    delivery_boy_wallet = models.ForeignKey(
        "wallet.DeliveryBoyWallet",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="wallet_transaction",
    )
    order = models.ForeignKey(
        "orders.Order",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_boy_order",
    )
    datetime = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(default=0.0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Current count
            current_count = (
                self.__class__.objects.aggregate(Max("id")).get("id__max") or 0
            )
            self.reference = "{}{:010d}".format(
                "COD-", current_count + 1 if current_count is not None else 1
            )
        return super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)
