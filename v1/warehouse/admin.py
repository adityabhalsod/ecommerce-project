from base.admin import BaseAdmin
from django.conf import settings
from django.contrib import admin
from v1.warehouse.models import (
    Purchase,
    PurchaseMultiItem,
    StockTransfer,
    StockTransferMultiItem,
    StoreStockManagement,
    Supplier,
    Warehouse,
    WarehouseStockManagement,
)


@admin.register(Warehouse)
class WarehouseAdmin(BaseAdmin):
    list_filter = (
        "is_active",
        "city",
        "state",
        "pin_code",
    )
    search_fields = (
        "name",
        "city",
        "state",
        "country",
        "pin_code",
        "address",
    )
    list_display = (
        "pk",
        "name",
        "city",
        "state",
        "country",
        "pin_code",
        "address",
        "is_active",
    )


@admin.register(Supplier)
class SupplierAdmin(BaseAdmin):
    list_filter = (
        "mobile",
        "email",
        "city",
        "state",
        "pin_code",
    )
    search_fields = (
        "business_name",
        "mobile",
        "email",
        "gst_number",
        "address",
        "city",
        "state",
        "country",
        "pin_code",
    )
    list_display = (
        "pk",
        "business_name",
        "mobile",
        "email",
        "gst_number",
        "address",
        "city",
        "state",
        "country",
        "pin_code",
    )


@admin.register(StockTransferMultiItem)
class StockTransferMultiItemAdmin(BaseAdmin):
    list_display = ("pk", "product_and_variation", "quantity")


@admin.register(Purchase)
class PurchaseAdmin(BaseAdmin):
    filter_horizontal = ["multiple_item"]
    list_filter = (
        "reference_number",
        "warehouse",
        "discount",
        "purchase_total",
        "discount_type",
    )
    search_fields = (
        "item_supplier",
        "reference_number",
        "datetime",
        "warehouse",
        "attach_document",
        "total_items",
        "sub_total",
        "additional_shipping_charges",
        "additional_notes",
        "discount_type",
        "tax",
        "discount",
        "purchase_total",
    )
    list_display = (
        "pk",
        "item_supplier",
        "reference_number",
        "datetime",
        "warehouse",
        "attach_document",
        "total_items",
        "sub_total",
        "additional_shipping_charges",
        "additional_notes",
        "discount_type",
        "tax",
        "discount",
        "purchase_total",
    )


@admin.register(PurchaseMultiItem)
class PurchaseMultiItemAdmin(BaseAdmin):
    list_filter = (
        "price",
        "quantity",
        "unit_cost",
    )
    search_fields = (
        "product_and_variation",
        "price",
        "quantity",
        "unit_cost",
    )
    list_display = (
        "pk",
        "product_and_variation",
        "price",
        "quantity",
        "unit_cost",
    )


@admin.register(StockTransfer)
class StockTransferAdmin(BaseAdmin):
    filter_horizontal = ["multiple_item"]

    list_filter = (
        "datetime",
        "warehouse",
        "store",
    )
    search_fields = (
        "datetime",
        "warehouse",
        "store",
    )
    list_display = (
        "pk",
        "datetime",
        "warehouse",
        "store",
    )


@admin.register(WarehouseStockManagement)
class WarehouseStockManagementAdmin(BaseAdmin):
    search_fields = (
        "product_and_variation",
        "warehouse",
        "quantity",
    )
    list_display = (
        "pk",
        "product_and_variation",
        "warehouse",
        "quantity",
        "datetime",
    )
    exclude = ["purchase_reference"]

    if not settings.DEBUG:

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False


@admin.register(StoreStockManagement)
class StoreStockManagementAdmin(BaseAdmin):
    search_fields = (
        "product_and_variation",
        "store",
        "quantity",
    )
    list_display = (
        "pk",
        "product_and_variation",
        "store",
        "quantity",
        "datetime",
    )
    exclude = ["transfer_reference"]

    if not settings.DEBUG:

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False
