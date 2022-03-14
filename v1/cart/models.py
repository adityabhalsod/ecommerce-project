from django.contrib.gis.db import models
from base.models import BaseModel
from v1.membership.choice import MembershipTypeChoices
from v1.cart.choice import OrderType


class Cart(BaseModel):
    store = models.ForeignKey(
        "store.Store",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="store_cart",
    )
    product_variation = models.ForeignKey(
        "catalog.Variation",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="cart_product_variation",
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    customer = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="customer_cart",
    )

    def __str__(self):
        return str(self.pk)


class Checkout(BaseModel):
    store = models.ForeignKey(
        "store.Store",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="store_checkout",
    )
    customer = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="customer_checkout",
    )
    discount_and_voucher = models.ForeignKey(
        "promotion.DiscountVoucher",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="checkout_discount_and_voucher",
    )
    final_amount = models.FloatField(
        default=0.0, null=True, blank=True
    )  # Before tax and other charge and discount
    final_quantity = models.IntegerField(default=0, null=True, blank=True)
    final_tax = models.FloatField(default=0.0, null=True, blank=True)
    final_discount = models.FloatField(default=0.0, null=True, blank=True)
    final_delivery_charge = models.FloatField(default=0.0, null=True, blank=True)
    final_delivery_boy_tip = models.FloatField(default=0.0, null=True, blank=True)
    final_membership_fee = models.FloatField(default=0.0, null=True, blank=True)
    final_total = models.FloatField(
        default=0.0, null=True, blank=True
    )  # After tax and other charge and discount
    no_contact_delivery = models.BooleanField(default=False)
    new_membership_adding = models.BooleanField(default=False)
    our_store_saving = models.FloatField(default=0.0, null=True, blank=True)
    membership_saving = models.FloatField(default=0.0, null=True, blank=True)
    order_type = models.CharField(
        max_length=255, choices=OrderType.choices, default=OrderType.ONLINE
    )
    membership_type = models.CharField(
        max_length=255,
        choices=MembershipTypeChoices.choices,
        default=MembershipTypeChoices.NOT_ATTEMPT,
    )
    order = models.ForeignKey(
        "orders.Order",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="checkout_order",
    )

    def __str__(self):
        return str(self.pk)
