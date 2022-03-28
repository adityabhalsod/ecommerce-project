from django.contrib import admin
from base.admin import BaseAdmin
from v1.orders.models import (
    FinalDeliveredOrder,
    Order,
)


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_filter = (
        "customer__username",
        "store__store_number",
        "store__store_name",
        "delivery_boy__store__store_name",
        "delivery_boy__current_status",
        "order_status",
        "order_type",
        "payment_status",
        "new_membership_adding",
        "membership_type",
        "dropzone",
    )
    search_fields = (
        "customer__username",
        "store__store_number",
        "store__store_name",
        "delivery_boy__store__store_name",
        "delivery_boy__current_status",
        "order_number",
        "dropzone",
    )
    readonly_fields = (
        "order_number",
        "order_token",
    )

    list_display = (
        "order_number",
        "store",
        "customer",
        "order_date",
        "total_amount",
        "total_quantity",
        "order_status",
        "order_type",
        "payment_status",
        "refund_status",
        "no_contact_delivery",
        "final_delivery_boy_tip",
        "final_membership_fee",
        "our_store_saving",
        "new_membership_adding",
        "order_token",
        "package_size",
        "package_weight",
        "delivery_time_start",
        "delivery_time_end",
        "membership_saving",
        "membership_type",
        "dropzone",
    )


@admin.register(FinalDeliveredOrder)
class FinalDeliveredOrderAdmin(BaseAdmin):
    list_filter = (
        "order",
        "customer",
        "store",
    )

    list_display = (
        "pk",
        "order",
        "rate",
        "quantity",
        "amount",
    )
