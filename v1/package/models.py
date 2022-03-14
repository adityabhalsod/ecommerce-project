from django.contrib.gis.db import models
from base.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField


class PackageBoy(BaseModel):
    user = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="package_user",
    )
    store = models.ForeignKey(
        "store.Store",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="store_package_user",
    )
    mobile_number = PhoneNumberField(
        "mobile number", unique=True, max_length=15, region="IN"
    )
    is_approve = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) if self.user else str(self.pk)
