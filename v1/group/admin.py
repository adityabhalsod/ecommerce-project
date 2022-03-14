from django.contrib import admin
from base.admin import BaseAdmin, BaseModelAdmin
from v1.group.models import (
    Collection,
    Color,
    GroupStructure,
    MultiplePhotos,
    ProductCollection,
)


@admin.register(Color)
class ColorAdmin(BaseAdmin):
    search_fields = (
        "name",
        "key",
    )

    list_display = (
        "pk",
        "name",
        "key",
        "image",
    )


# from v1.group.models import GroupType
# @admin.register(GroupType)
# class GroupTypeAdmin(BaseAdmin):
#     list_filter = ("is_active",)
#     search_fields = ("type","display",)

#     list_display = (
#         "display",
#         "type",
#         "is_active",
#     )


@admin.register(MultiplePhotos)
class MultiplePhotosAdmin(BaseAdmin):
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


@admin.register(GroupStructure)
class GroupStructureAdmin(BaseAdmin):
    filter_horizontal = [
        "store",
        "multiple_photos",
    ]
    readonly_fields = (
        "webp_image",
        "thumbnail",
    )
    list_filter = (
        "is_active",
        "store__store_name",
        "background_color__name",
    )
    search_fields = (
        "sequence",
        "group_name",
        "background_color__name",
        "short_text",
        "long_text",
        "redirection_key",
    )

    list_display = (
        "pk",
        "group_name",
        "sequence",
        "is_active",
        "level",
    )


class ProductCollectionModelAdmin(BaseModelAdmin):
    model = ProductCollection
    extra = 1


@admin.register(Collection)
class CollectionAdmin(BaseAdmin):
    inlines = [
        ProductCollectionModelAdmin,
    ]

    list_filter = (
        "alignment",
        "group__group_name",
    )
    search_fields = ("alignment",)

    def group_name(self):
        if self.group and self.group.group_name:
            return str(self.group.group_name)
        else:
            return "N/A"

    list_display = (
        "pk",
        group_name,
        "sequence",
        "alignment",
    )


@admin.register(ProductCollection)
class ProductCollectionAdmin(BaseAdmin):
    list_filter = ("collection__group__group_name",)
    search_fields = (
        "product__item_name",
        "background__name",
        "bottem_line__name",
    )

    def product_name(self):
        if self.product and self.product.item_name:
            return str(self.product.item_name)
        else:
            return "N/A"

    def collection_alignment(self):
        if self.collection and self.collection.alignment:
            return str(self.collection.alignment)
        else:
            return "N/A"

    def background(self):
        if self.background_color and self.background_color.name:
            return str(self.background_color.name)
        else:
            return "N/A"

    def bottem_line(self):
        if self.bottem_line_color and self.bottem_line_color.name:
            return str(self.bottem_line_color.name)
        else:
            return "N/A"

    list_display = (
        "pk",
        product_name,
        collection_alignment,
        background,
        bottem_line,
        "sequence",
    )
