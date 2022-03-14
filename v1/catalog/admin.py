from django.contrib import admin
from base.admin import BaseAdmin, BaseModelAdmin
from v1.catalog.models import (
    Category,
    Product,
    ProductPhoto,
    ProductStockMaster,
    Unit,
    Variation,
    VariationPhoto,
)


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    readonly_fields = (
        "webp_image",
        "thumbnail",
    )
    search_fields = (
        "name",
        "description",
    )
    list_display = (
        "pk",
        "name",
        "sequence",
    )
    readonly_fields = ("slug",)


@admin.register(Unit)
class UnitAdmin(BaseAdmin):
    search_fields = (
        "name",
        "short_name",
    )

    list_display = (
        "pk",
        "name",
        "short_name",
    )


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    filter_horizontal = ["photos"]
    search_fields = (
        "item_code",
        "item_name",
        "bill_display_item_name",
        "short_description",
        "search_keyword",
    )
    list_filter = ("category",)
    list_display = (
        "pk",
        "item_code",
        "item_name",
        "bill_display_item_name",
    )
    readonly_fields = ("slug",)


@admin.register(Variation)
class VariationAdmin(BaseAdmin):
    filter_horizontal = ["photos"]
    readonly_fields = ("purchase_rate",)

    list_filter = (
        "name",
        "value",
    )

    search_fields = (
        "name",
        "value",
        "upc_barcode",
        "min_stock",
        "mrp",
        "our_rate",
        "member_rate",
        "purchase_rate",
        "exclusive_rate",
        "max_order_quantity",
        "open_stock",
    )

    list_display = (
        "pk",
        "name",
        "value",
        "upc_barcode",
        "hsn_code",
        "mrp",
        "our_rate",
        "member_rate",
        "purchase_rate",
        "exclusive_rate",
        "max_order_quantity",
        "open_stock",
    )


@admin.register(VariationPhoto)
class VariationPhotoAdmin(BaseAdmin):
    readonly_fields = (
        "webp_image",
        "thumbnail",
    )
    search_fields = (
        "alt_text",
        "is_default",
    )

    list_display = (
        "pk",
        "original",
        "webp_image",
        "thumbnail",
        "alt_text",
        "is_default",
    )


@admin.register(ProductPhoto)
class ProductPhotoAdmin(BaseAdmin):
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
        "is_default",
    )


class VariationModelAdmin(BaseModelAdmin):
    filter_horizontal = ["photos"]
    readonly_fields = ("purchase_rate",)
    model = Variation
    extra = 1


@admin.register(ProductStockMaster)
class ProductStockMasterAdmin(BaseAdmin):
    inlines = [
        VariationModelAdmin,
    ]
    filter_horizontal = ["store"]
    list_filter = (
        "is_exclusive_item",
        "is_super_saving_item",
        "is_active_item",
        "store__store_name",
        "store__city",
        "store__state",
    )

    search_fields = (
        "product__item_code",
        "product__item_name",
        "product__bill_display_item_name",
        "store__store_number",
        "store__store_name",
        "store__city",
        "store__state",
        "store__pin_code",
        "position",
    )

    list_display = (
        "pk",
        "one_rs_store",
        "is_active_item",
        "is_exclusive_item",
        "type",
        "position",
        "row",
        "rack",
    )
