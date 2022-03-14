from django.contrib import admin

from base.admin import BaseAdmin

from .models import Membership, MembershipBenefits, MembershipPlain

# Register your models here.


@admin.register(Membership)
class MembershipAdmin(BaseAdmin):
    search_fields = ("customer__username",)
    list_filter = (
        "plan",
        "is_active",
    )
    list_display = (
        "pk",
        "amount",
        "plan",
        "start_at",
        "end_at",
        "is_active",
    )


@admin.register(MembershipBenefits)
class MembershipBenefitsAdmin(BaseAdmin):
    search_fields = ("text",)
    list_filter = ("is_active",)
    list_display = (
        "pk",
        "text",
        "is_active",
    )


@admin.register(MembershipPlain)
class MembershipPlainAdmin(BaseAdmin):
    filter_horizontal = ["benefits"]
    search_fields = ("benefits__text",)
    list_filter = (
        "is_active",
        "type",
    )
    list_display = (
        "pk",
        "type",
        "mrp_amount",
        "discount_amount",
        "is_active",
    )
