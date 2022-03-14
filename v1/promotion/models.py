from ckeditor.fields import RichTextField
from django.contrib.gis.db import models
from django.db.models import Max
from django.utils import timezone
from base.models import BaseModel
from v1.promotion.choice import ValueType, VoucherType


class DiscountVoucher(BaseModel):
    type = models.CharField(
        max_length=20, choices=VoucherType.choices, default=VoucherType.ENTIRE_ORDER
    )
    code = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(default="")
    is_code_required = models.BooleanField(default=False)

    min_amount = models.FloatField(default=0.0)
    is_exist_min_amount = models.BooleanField(default=False)

    discount_value = models.FloatField(default=0.0)

    value_type = models.CharField(
        max_length=10,
        choices=ValueType.choices,
        default=ValueType.FIXED,
    )

    is_apply_super_saving_days_item = models.BooleanField(default=False)
    is_apply_exclusive_offer_item = models.BooleanField(default=False)
    is_apply_free_delivery = models.BooleanField(default=False)

    min_checkout_items_quantity = models.PositiveIntegerField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used = models.PositiveIntegerField(default=0, editable=False)

    priority = models.BigIntegerField(default=0, null=True, blank=True)

    store = models.ManyToManyField(
        "store.Store", blank=True, related_name="store_coupon"
    )
    products = models.ManyToManyField(
        "catalog.Product", blank=True, related_name="product_coupon"
    )
    variants = models.ManyToManyField(
        "catalog.Variation", blank=True, related_name="variation_coupon"
    )
    categories = models.ManyToManyField(
        "catalog.Category", blank=True, related_name="category_coupon"
    )

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    terms_and_conditions = RichTextField(default="")

    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding and self.is_active:
            # Current count
            current_count = self.current_active_priority()
            # sequence
            self.priority = current_count + 1

        return super(DiscountVoucher, self).save(*args, **kwargs)

    def current_active_priority(self, set=False):
        current_count = (
            self.__class__.objects.filter(is_active=True)
            .aggregate(Max("priority"))
            .get("priority__max")
            or 0
        )
        if set:
            # sequence
            self.priority = current_count + 1
            self.save()
            return self.priority
        return current_count

    def __str__(self):
        return str(self.pk)


class ReferralAndEarn(BaseModel):
    refer_customer = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="refer_customer_user",
    )
    customer = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="customer_user",
    )
    referral_code = models.CharField(max_length=255, blank=True)
    earn_amount = models.FloatField(default=0.0)
    transaction = models.ForeignKey(
        "wallet.Transaction",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="wallet_transaction",
    )

    class Meta:
        unique_together = [
            ("refer_customer", "customer"),  # one refer code using only first time.
            ("referral_code", "customer"),  # same code not apply in 2nd time.
            ("customer",),  # one customer are not set many refer customer.
        ]

    def save(self, *args, **kwargs):
        return super(ReferralAndEarn, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)
