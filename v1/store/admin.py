from django.contrib import admin
from base.admin import BaseAdmin
from v1.store.models import (
    Store,
)


@admin.register(Store)
class StoreAdmin(BaseAdmin):
    list_filter = (
        "store_number",
        "store_name",
        "city",
        "state",
    )
    search_fields = (
        "store_number",
        "store_name",
        "city",
        "state",
        "pin_code",
        "manager__username",
    )
    readonly_fields = (
        "slug",
        "store_number",
    )

    def manager_username(self):
        if self.manager and self.manager.username:
            return str(self.manager.username)
        else:
            return "N/A"

    list_display = (
        "pk",
        "store_name",
        manager_username,
        "is_active",
        "is_open",
    )
