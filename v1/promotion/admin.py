from django.contrib import admin

from base.admin import BaseAdmin
from v1.promotion.models import DiscountVoucher, ReferralAndEarn


@admin.register(DiscountVoucher)
class DiscountVoucherAdmin(BaseAdmin):
    filter_horizontal = [
        "store",
        "products",
        "variants",
        "categories",
    ]

    list_filter = (
        "type",
        "is_exist_min_amount",
        "discount_value",
        "value_type",
        "is_apply_super_saving_days_item",
        "is_apply_exclusive_offer_item",
        "is_apply_free_delivery",
        "min_checkout_items_quantity",
        "usage_limit",
        "used",
        "is_active",
    )
    search_fields = (
        "name",
        "code",
        "discount_value",
        "value_type",
    )

    list_display = (
        "pk",
        "name",
        "discount_value",
        "code",
        "is_code_required",
        "priority",
        "min_amount",
        "is_exist_min_amount",
        "discount_value",
        "value_type",
        "is_apply_super_saving_days_item",
        "is_apply_exclusive_offer_item",
        "is_apply_free_delivery",
        "min_checkout_items_quantity",
        "usage_limit",
        "used",
        "start_date",
        "end_date",
        "is_active",
    )


@admin.register(ReferralAndEarn)
class ReferalAndEarnAdmin(BaseAdmin):
    search_fields = (
        "refer_customer__first_name",
        "refer_customer__last_name",
        "refer_customer__username",
        "customer__first_name",
        "customer__last_name",
        "customer__username",
        "referral_code",
        "earn_amount",
    )

    list_display = (
        "pk",
        "refer_customer",
        "customer",
        "referral_code",
        "earn_amount",
    )
