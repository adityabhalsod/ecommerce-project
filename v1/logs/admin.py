from django.contrib import admin
from base.admin import BaseAdmin

from v1.logs.models import Log

# Register your models here.
@admin.register(Log)
class LogsAdmin(BaseAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_filter = (
        "http_code",
        "http_method",
        "remote_address",
    )

    search_fields = (
        "http_code",
        "http_method",
        "body_request",
        "body_response",
        "traceback",
        "remote_address",
        "endpoint",
        "latency_time",
        "body_response_size",
    )

    list_display = (
        "pk",
        "http_code",
        "http_method",
        "remote_address",
        "endpoint",
        "latency_time",
        "body_response_size",
    )
