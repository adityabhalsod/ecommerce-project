from django.contrib import admin
from base.admin import BaseAdmin

from v1.wallet.models import (
    CaseOnDeliveryCollectionHistory,
    CustomerWallet,
    DeliveryBoyWallet,
    Transaction,
)
from django.conf import settings


@admin.register(CustomerWallet)
class CustomerWalletAdmin(BaseAdmin):
    if not settings.DEBUG:

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

    list_filter = ("is_active",)

    list_display = (
        "pk",
        "balance_amount",
        "is_active",
    )


@admin.register(DeliveryBoyWallet)
class DeliveryBoyWalletAdmin(BaseAdmin):
    if not settings.DEBUG:

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

    list_filter = ("is_active",)

    list_display = (
        "pk",
        "balance_amount",
        "is_active",
    )


@admin.register(Transaction)
class TransactionAdmin(BaseAdmin):
    if not settings.DEBUG:

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

    list_filter = (
        "transaction_type",
        "method",
        "status",
        "platform",
    )
    search_fields = (
        "name",
        "notes",
        "amount",
    )

    list_display = (
        "pk",
        "name",
        "transaction_type",
        "method",
        "status",
        "platform",
        "datetime",
        "amount",
    )


@admin.register(CaseOnDeliveryCollectionHistory)
class CaseOnDeliveryCollectionHistoryAdmin(BaseAdmin):
    if not settings.DEBUG:

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

    search_fields = (
        "name",
        "notes",
        "amount",
    )

    list_display = (
        "pk",
        "name",
        "notes",
        "datetime",
        "amount",
    )
