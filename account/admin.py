from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from account.forms import PermissionModelForm

from account.models import (
    Address,
    BannedIP,
    UntrackedUserAgent,
    User,
    UserEmail,
    UserMobileNumber,
    UserPhotos,
    Visitor,
)
from base.admin import BaseAdmin, BaseModelAdmin

# Unregister the original Group admin.
admin.site.unregister(Group)


class AddressModelAdmin(BaseModelAdmin):
    model = Address
    extra = 1


class UserPhotosModelAdmin(BaseModelAdmin):
    model = UserPhotos
    extra = 1


class UserMobileNumberModelAdmin(BaseModelAdmin):
    model = UserMobileNumber
    extra = 1


class UserEmailModelAdmin(BaseModelAdmin):
    model = UserEmail
    extra = 1


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    readonly_fields = (
        "username",
        "referral_code",
        "is_online",
    )
    inlines = [
        AddressModelAdmin,
        UserPhotosModelAdmin,
        UserMobileNumberModelAdmin,
        UserEmailModelAdmin,
    ]
    fieldsets = None
    filter_horizontal = ["groups"]
    list_filter = (
        "is_superuser",
        "is_active",
        "is_deleted",
        "is_profile_completely_filled",
        "groups",
        "is_online",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "is_online",
    )
    list_display = (
        "pk",
        "is_superuser",
        "username",
        "first_name",
        "father_name",
        "referral_code",
        "last_name",
        "date_of_birth",
        "is_profile_completely_filled",
        "is_active",
        "is_deleted",
        "is_online",
    )
    exclude = ("user_permissions",)


@admin.register(UserEmail)
class EmailAdmin(BaseAdmin):
    list_filter = (
        "user__groups",
        "verify",
        "primary",
    )
    search_fields = (
        "email",
        "verify",
        "primary",
    )
    list_display = (
        "pk",
        "email",
        "verify",
        "primary",
    )


@admin.register(UserMobileNumber)
class UserMobileNumberAdmin(BaseAdmin):
    list_filter = (
        "user__groups",
        "verify",
        "primary",
    )
    search_fields = (
        "mobile_number",
        "verify",
        "primary",
    )
    list_display = (
        "pk",
        "mobile_number",
        "verify",
        "primary",
    )


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    list_filter = (
        "address_type",
        "is_billing",
        "is_set_manually",
        "street_name",
        "land_mark",
    )
    search_fields = (
        "address",
        "verify",
        "primary",
        "house_number_and_building_name",
        "street_name",
        "land_mark",
    )
    list_display = (
        "pk",
        "city",
        "house_number_and_building_name",
        "street_name",
        "land_mark",
        "state",
        "country",
        "pin_code",
        "address_type",
        "primary",
        "is_billing",
        "is_set_manually",
    )


# Create a new Group admin.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = PermissionModelForm
    # Filter permissions horizontal as well.
    filter_horizontal = ["permissions"]


@admin.register(BannedIP)
class BannedIPAdmin(BaseAdmin):
    search_fields = ("ip_address",)


@admin.register(UntrackedUserAgent)
class UntrackedUserAgentAdmin(BaseAdmin):
    search_fields = ("keyword",)


@admin.register(Visitor)
class VisitorAdmin(BaseAdmin):
    list_filter = (
        "user",
        "is_deleted",
        "user_agent",
    )
    search_fields = ("ip_address", "user", "user_agent", "url")
