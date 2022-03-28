from django.contrib import admin
from base.admin import BaseAdmin
from v1.delivery.models import (
    DeliveryBoy,
    DeliveryBoyDocument,
    DeliveryBoyPayoutInformation,
    DeliveryBoyReview,
    DeliveryBoyVehicleInformation,
    DeliveryBoyVehiclePhotos,
    DeliveryCharges,
)


@admin.register(DeliveryBoy)
class DeliveryBoyAdmin(BaseAdmin):
    list_filter = (
        "status",
        "current_status",
        "store__store_number",
        "store__store_name",
        "store__city",
        "store__state",
    )
    search_fields = (
        "store__store_number",
        "store__store_name",
        "store__city",
        "store__state",
        "store__pin_code",
        "user__username",
    )

    def username(self):
        if self.user and self.user.username:
            return str(self.user.username)
        else:
            return "N/A"

    list_display = (
        "pk",
        username,
        "current_status",
        "payout_balance",
    )


@admin.register(DeliveryBoyVehiclePhotos)
class DeliveryBoyVehiclePhotosAdmin(BaseAdmin):
    readonly_fields = (
        "webp_image",
        "thumbnail",
    )
    search_fields = ("alt_text",)

    list_display = (
        "pk",
        "original",
        "webp_image",
        "thumbnail",
        "alt_text",
    )


@admin.register(DeliveryBoyVehicleInformation)
class DeliveryBoyVehicleInformationAdmin(BaseAdmin):
    filter_horizontal = ["photos"]
    list_filter = (
        "vehicle_type",
        "delivery_boy__store__store_name",
        "delivery_boy__status",
        "delivery_boy__current_status",
    )
    search_fields = (
        "vehicle_type",
        "delivery_boy__user__username",
        "delivery_boy__store__store_name",
        "delivery_boy__current_status",
        "vehicle_number",
    )

    def username(self):
        if (
            self.delivery_boy
            and self.delivery_boy.user
            and self.delivery_boy.user.username
        ):
            return str(self.delivery_boy.user.username)
        else:
            return "N/A"

    def store_name(self):
        if (
            self.delivery_boy
            and self.delivery_boy.store
            and self.delivery_boy.store.store_name
        ):
            return str(self.delivery_boy.store.store_name)
        else:
            return "N/A"

    list_display = (
        "pk",
        username,
        store_name,
        "vehicle_type",
    )


@admin.register(DeliveryBoyDocument)
class DeliveryBoyDocumentAdmin(BaseAdmin):
    list_filter = (
        "document_type",
        "delivery_boy__store__store_name",
        "delivery_boy__current_status",
        "delivery_boy__status",
        "status",
    )
    search_fields = (
        "delivery_boy__user__username",
        "delivery_boy__store__store_name",
        "delivery_boy__current_status",
        "document_id_number",
    )

    def username(self):
        if (
            self.delivery_boy
            and self.delivery_boy.user
            and self.delivery_boy.user.username
        ):
            return str(self.delivery_boy.user.username)
        else:
            return "N/A"

    def store_name(self):
        if (
            self.delivery_boy
            and self.delivery_boy.store
            and self.delivery_boy.store.store_name
        ):
            return str(self.delivery_boy.store.store_name)
        else:
            return "N/A"

    list_display = (
        "pk",
        username,
        store_name,
        "document_id_number",
        "document_type",
        "status",
    )


@admin.register(DeliveryBoyReview)
class DeliveryBoyReviewAdmin(BaseAdmin):
    list_filter = (
        "rating",
        "delivery_boy__store__store_name",
        "delivery_boy__status",
        "delivery_boy__current_status",
    )
    search_fields = (
        "delivery_boy__user__username",
        "delivery_boy__store__store_name",
        "delivery_boy__current_status",
        "author__username",
    )

    def author_username(self):
        if self.author.user and self.author.user.username:
            return str(self.author.user.username)
        else:
            return "N/A"

    def username(self):
        if (
            self.delivery_boy
            and self.delivery_boy.user
            and self.delivery_boy.user.username
        ):
            return str(self.delivery_boy.user.username)
        else:
            return "N/A"

    def store_name(self):
        if (
            self.delivery_boy
            and self.delivery_boy.store
            and self.delivery_boy.store.store_name
        ):
            return str(self.delivery_boy.store.store_name)
        else:
            return "N/A"

    list_display = (
        "pk",
        author_username,
        username,
        store_name,
        "title",
        "rating",
    )


@admin.register(DeliveryBoyPayoutInformation)
class DeliveryBoyPayoutInformationAdmin(BaseAdmin):
    list_filter = (
        "delivery_boy__store__store_name",
        "delivery_boy__status",
        "delivery_boy__current_status",
    )
    search_fields = (
        "delivery_boy__user__username",
        "delivery_boy__store__store_name",
        "delivery_boy__current_status",
        "bank_account_ifsc_code",
        "bank_account_number",
        "bank_account_name",
        "bank_branch_name",
        "bank_branch_address",
        "payout_balance",
    )

    def username(self):
        if (
            self.delivery_boy
            and self.delivery_boy.user
            and self.delivery_boy.user.username
        ):
            return str(self.delivery_boy.user.username)
        else:
            return "N/A"

    def store_name(self):
        if (
            self.delivery_boy
            and self.delivery_boy.store
            and self.delivery_boy.store.store_name
        ):
            return str(self.delivery_boy.store.store_name)
        else:
            return "N/A"

    list_display = (
        "pk",
        username,
        store_name,
        "bank_account_ifsc_code",
        "bank_account_number",
        "payout_balance",
    )


@admin.register(DeliveryCharges)
class DeliveryChargesAdmin(BaseAdmin):
    list_filter = ("is_active",)
    search_fields = (
        "title",
        "amount_starting_range",
        "amount_ending_range",
        "delivery_charge",
        "is_active",
    )
    list_display = (
        "pk",
        "title",
        "amount_starting_range",
        "amount_ending_range",
        "delivery_charge",
        "is_active",
    )
