from base.models import BaseModel
from django.contrib.gis.db import models
from django.db.models import Max
from django.utils import timezone
from v1.membership.choice import MembershipTypeChoices
from v1.orders.choice import OrderStatus, OrderType, PaymentStatus, RefundStatus


class Order(BaseModel):
    customer = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="customer",
    )
    billing_address = models.TextField(null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    store = models.ForeignKey(
        "store.Store",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="store_order",
    )
    transaction = models.ForeignKey(
        "wallet.Transaction",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="order_transaction",
    )
    order_number = models.CharField(default="", max_length=255, null=True, blank=True)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.FloatField(default=0.0, null=True, blank=True)
    collect_amount = models.FloatField(default=0.0, null=True, blank=True)
    wallet_amount_used = models.FloatField(default=0.0, null=True, blank=True)
    total_quantity = models.IntegerField(default=0, null=True, blank=True)
    order_status = models.CharField(
        max_length=255, choices=OrderStatus.choices, default=OrderStatus.NOT_ATTEMPT
    )
    order_type = models.CharField(
        max_length=255, choices=OrderType.choices, default=OrderType.NOT_ATTEMPT
    )
    refund_status = models.CharField(
        max_length=255, choices=RefundStatus.choices, default=RefundStatus.NOT_ATTEMPT
    )
    payment_status = models.CharField(
        max_length=255, choices=PaymentStatus.choices, default=PaymentStatus.WATING
    )

    package_size = models.CharField(default="", max_length=255, null=True, blank=True)
    package_weight = models.CharField(default="", max_length=255, null=True, blank=True)

    delivery_boy = models.ForeignKey(
        "delivery.DeliveryBoy",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="order_delivered",
    )
    package_boy = models.ForeignKey(
        "package.PackageBoy",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="order_pack",
    )
    discount_and_voucher = models.ForeignKey(
        "promotion.DiscountVoucher",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="order_discount_and_voucher",
    )
    delivery_time_start = models.TimeField(blank=True, null=True)
    delivery_time_end = models.TimeField(blank=True, null=True)
    package_time_start = models.TimeField(blank=True, null=True)
    package_time_end = models.TimeField(blank=True, null=True)
    no_contact_delivery = models.BooleanField(default=False)
    sequence = models.BigIntegerField(default=0, null=True, blank=True)
    final_delivery_boy_tip = models.FloatField(default=0.0, null=True, blank=True)

    final_membership_fee = models.FloatField(default=0.0, null=True, blank=True)
    new_membership_adding = models.BooleanField(default=False)

    our_store_saving = models.FloatField(default=0.0, null=True, blank=True)
    membership_saving = models.FloatField(default=0.0, null=True, blank=True)
    order_token = models.TextField(default="", null=True, blank=True)
    membership_type = models.CharField(
        max_length=255,
        choices=MembershipTypeChoices.choices,
        default=MembershipTypeChoices.NOT_ATTEMPT,
    )
    dropzone = models.CharField(default="", max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Current count
            current_count = (
                self.__class__.objects.aggregate(Max("sequence")).get("sequence__max")
                or 0
            )

            # sequence
            self.sequence = current_count + 1

        # Auto calculated order number
        if self.store and self.store.store_number and not self.order_number:
            order_num = 1000 + self.sequence
            self.order_number = (
                "Q" + str(order_num) + "-" + str(self.store.store_number)
            )

        # Set collection amount
        if self.wallet_amount_used and self.wallet_amount_used != 0.0:
            calculation_collect_amount = float(self.total_amount) - float(
                self.wallet_amount_used
            )
            if calculation_collect_amount > 0.0:
                self.collect_amount = calculation_collect_amount

        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order_number) if self.order_number else str(self.pk)


class FinalDeliveredOrder(BaseModel):
    customer = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="customer_delivered_order",
    )
    store = models.ForeignKey(
        "store.Store",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="store_order_delivered_order",
    )
    product_variation = models.ForeignKey(
        "catalog.Variation",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="product_variation_delivered_order",
    )
    order = models.ForeignKey(
        "orders.Order",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="final_delivered_order",
    )
    checkout = models.ForeignKey(
        "cart.Checkout",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="checkout_delivered_order",
    )
    rate = models.FloatField(default=0.0, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    discount_and_voucher = models.ForeignKey(
        "promotion.DiscountVoucher",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="individual_discount_and_voucher",
    )

    def __str__(self):
        return str(self.pk)
