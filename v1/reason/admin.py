from django.contrib import admin
from base.admin import BaseAdmin
from v1.reason.models import Reason, ReasonType


@admin.register(ReasonType)
class ReasonTypeAdmin(BaseAdmin):
    search_fields = ("type",)
    list_display = (
        "pk",
        "type",
    )


@admin.register(Reason)
class ReasonAdmin(BaseAdmin):
    list_filter = (
        "is_approve_by_admin",
        "reason_for__type",
    )
    search_fields = (
        "user__username",
        "reason_for__type",
        "text",
    )

    def username(self):
        if self.create_by and self.create_by.username:
            return str(self.create_by.username)
        else:
            return "N/A"

    def reason_type(self):
        if self.reason_for and self.reason_for.type:
            return str(self.reason_for.type)
        else:
            return "N/A"

    list_display = ("pk", username, reason_type)
