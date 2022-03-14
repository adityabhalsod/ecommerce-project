from django.contrib import admin
from base.admin import BaseAdmin
from v1.package.models import PackageBoy


@admin.register(PackageBoy)
class PackageBoyAdmin(BaseAdmin):
    list_filter = (
        "user__username",
        "store__store_number",
        "store__store_name",
    )
    search_fields = (
        "user__username",
        "store__store_number",
        "store__store_name",
    )

    list_display = (
        "pk",
        "store",
        "user",
        "mobile_number",
        "is_approve",
    )
