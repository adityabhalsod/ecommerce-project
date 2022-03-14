from django.contrib.gis.db import models
from base.models import BaseModel
from v1.membership.choice import MembershipTypeChoices


class Membership(BaseModel):
    customer = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="customer_membership",
    )
    plan = models.ForeignKey(
        "membership.MembershipPlain",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="customer_membership_plan",
    )
    amount = models.FloatField(default=0.0, null=True, blank=True)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    transaction = models.ForeignKey(
        "wallet.Transaction",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="membership_transaction",
    )
    payment_token = models.TextField(default="", null=True, blank=True)

    class Meta:
        unique_together = [
            ("customer",),
        ]

    def __str__(self):
        return str(self.pk)


class MembershipPlain(BaseModel):
    benefits = models.ManyToManyField(
        "membership.MembershipBenefits",
        blank=True,
        related_name="plan_benefits",
    )
    type = models.CharField(
        max_length=255,
        choices=MembershipTypeChoices.choices,
        default=MembershipTypeChoices.ONE_MONTH,
    )
    mrp_amount = models.FloatField(default=0.0, null=True, blank=True)
    discount_amount = models.FloatField(default=0.0, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.discount_amount:
            self.discount_amount = self.mrp_amount

        if self.is_active:
            old_active = self.__class__.objects.filter(
                type=self.type, is_active=True
            ).first()
            if old_active:
                old_active.is_active = False
                old_active.save()
        return super(MembershipPlain, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.type)

    @property
    def discount_calculated(self):
        if self.mrp_amount and self.discount_amount:
            try:
                return (float(self.discount_amount) / float(self.mrp_amount)) * 100.00
            except Exception:
                return 0.0
        return 0.0


class MembershipBenefits(BaseModel):
    text = models.TextField(default="", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.text)
