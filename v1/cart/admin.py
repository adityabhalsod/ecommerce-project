from django.contrib import admin
from base.admin import BaseAdmin
from v1.cart.models import Cart, Checkout


@admin.register(Cart)
class CartAdmin(BaseAdmin):
    search_fields = (
        "customer__username",
        "product_variation__product_stock_master__is_exclusive_item",
        "product_variation__product_stock_master__is_super_saving_item",
        "product_variation__product_stock_master__product__item_code",
        "product_variation__product_stock_master__product__item_name",
        "product_variation__product_stock_master__product__bill_display_item_name",
        "product_variation__product_stock_master__product__hsn_code",
        "product_variation__product_stock_master__store__store_number",
        "product_variation__product_stock_master__store__store_name",
        "product_variation__product_stock_master__store__city",
        "product_variation__product_stock_master__store__state",
        "product_variation__product_stock_master__store__pin_code",
    )
    list_filter = (
        "customer__username",
        "product_variation__product_stock_master__is_exclusive_item",
        "product_variation__product_stock_master__is_super_saving_item",
        "product_variation__product_stock_master__is_active_item",
        "product_variation__product_stock_master__product__item_code",
        "product_variation__product_stock_master__product__item_name",
        "product_variation__product_stock_master__product__bill_display_item_name",
        "product_variation__product_stock_master__store__store_number",
        "product_variation__product_stock_master__store__store_name",
        "product_variation__product_stock_master__store__city",
        "product_variation__product_stock_master__store__state",
        "product_variation__product_stock_master__store__pin_code",
    )
    list_display = (
        "pk",
        "customer",
        "product_variation",
        "quantity",
    )


@admin.register(Checkout)
class CheckoutAdmin(BaseAdmin):
    search_fields = ("customer__username",)
    list_filter = ("customer__username",)
    list_display = (
        "pk",
        "customer",
        "final_total",
        "final_discount",
        "final_delivery_charge",
        "final_amount",
    )
