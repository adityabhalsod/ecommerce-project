from django.contrib.gis.db import models
from base.models import BaseModel


class ReasonType(BaseModel):
    type = models.CharField(default="", max_length=255, null=True, blank=True)


class Reason(BaseModel):
    create_by = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="reason_create_by",
    )
    text = models.TextField(default="", null=True, blank=True)
    is_approve_by_admin = models.BooleanField(default=False)
    reason_for = models.ForeignKey(
        "reason.ReasonType",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="reason_type",
    )

    def __str__(self):
        return str(self.pk)
