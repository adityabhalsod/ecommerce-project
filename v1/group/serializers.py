from django.utils.translation import ugettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from base.serializers import BaseSerializer, PassObject
from v1.catalog.models import Product
from v1.store.models import Store
from v1.store.serializers import StoreExcloudGeoLocationSerializer
from v1.catalog.serializers import (
    AllProductSerializer,
    ProductCRUDSerializer,
)

from .models import (
    Collection,
    Color,
    GroupStructure,
    GroupType,
    MultiplePhotos,
    ProductCollection,
)


class GroupTypeCRUDSerializer(BaseSerializer):
    class Meta:
        model = GroupType
        fields = "__all__"


class ColorCRUDSerializer(BaseSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Color
        fields = "__all__"


class CollectionSerializer(BaseSerializer):
    class Meta:
        model = Collection
        fields = (
            "id",
            "alignment",
            "sequence",
        )


class MultiplePhotosCRUDSerializer(BaseSerializer):
    original = Base64ImageField(required=False)

    class Meta:
        model = MultiplePhotos
        fields = "__all__"


class GroupStructureCRUDSerializer(BaseSerializer):
    store = StoreExcloudGeoLocationSerializer(read_only=True, many=True)
    store_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        many=True,
        write_only=True,
    )

    sub_group = serializers.SerializerMethodField(read_only=True)
    parent_group_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=GroupStructure.objects.exclude(is_deleted=True),
        source="parent_group",
        write_only=True,
    )

    background_color = ColorCRUDSerializer(required=False)
    background_color_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Color.objects.exclude(is_deleted=True),
        source="background_color",
        write_only=True,
    )

    bottem_line_color = ColorCRUDSerializer(required=False)
    bottem_line_color_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Color.objects.exclude(is_deleted=True),
        source="bottem_line_color",
        write_only=True,
    )

    self_identify = GroupTypeCRUDSerializer(required=False)
    self_identify_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=GroupType.objects.exclude(is_deleted=True),
        source="self_identify",
        write_only=True,
    )
    image = Base64ImageField(required=False)
    multiple_photos = MultiplePhotosCRUDSerializer(read_only=True, many=True)
    multiple_photos_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=MultiplePhotos.objects.exclude(is_deleted=True),
        source="multiple_photos",
        write_only=True,
        many=True,
    )

    collection = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GroupStructure
        fields = "__all__"
        read_only_fields = (
            "slug",
            "sequence",
            "is_main",
        )

    def get_sub_group(self, obj):
        sub_group = obj.children.exclude(is_deleted=True).order_by("sequence")
        if not sub_group:
            return []
        return GroupStructureCRUDSerializer(
            sub_group, many=True, context={"request": self.context.get("request")}
        ).data

    def get_collection(self, obj):
        sub_collection = obj.group_collection.exclude(is_deleted=True).order_by(
            "sequence"
        )
        if not sub_collection:
            return []
        return CollectionSerializer(
            sub_collection, many=True, context={"request": self.context.get("request")}
        ).data


class GroupStructureAdminCRUDSerializer(BaseSerializer):
    store = StoreExcloudGeoLocationSerializer(read_only=True, many=True)
    store_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        many=True,
        write_only=True,
    )
    parent_group_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=GroupStructure.objects.exclude(is_deleted=True),
        source="parent_group",
        write_only=True,
    )

    background_color = ColorCRUDSerializer(required=False)
    background_color_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Color.objects.exclude(is_deleted=True),
        source="background_color",
        write_only=True,
    )

    bottem_line_color = ColorCRUDSerializer(required=False)
    bottem_line_color_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Color.objects.exclude(is_deleted=True),
        source="bottem_line_color",
        write_only=True,
    )

    self_identify = GroupTypeCRUDSerializer(required=False)
    self_identify_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=GroupType.objects.exclude(is_deleted=True),
        source="self_identify",
        write_only=True,
    )
    image = Base64ImageField(required=False)
    multiple_photos = MultiplePhotosCRUDSerializer(read_only=True, many=True)
    multiple_photos_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=MultiplePhotos.objects.exclude(is_deleted=True),
        source="multiple_photos",
        write_only=True,
        many=True,
    )

    class Meta:
        model = GroupStructure
        fields = "__all__"
        read_only_fields = (
            "slug",
            "sequence",
            "is_main",
        )


class CollectionCRUDSerializer(BaseSerializer):
    group = GroupStructureCRUDSerializer(read_only=True)
    group_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=GroupStructure.objects.exclude(is_deleted=True),
        source="group",
        write_only=True,
    )

    class Meta:
        model = Collection
        fields = "__all__"
        read_only_fields = ("sequence",)


class ProductCollectionCRUDSerializer(BaseSerializer):
    store = StoreExcloudGeoLocationSerializer(read_only=True)
    store_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        write_only=True,
    )
    background_color = ColorCRUDSerializer(required=False)
    background_color_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Color.objects.exclude(is_deleted=True),
        source="background_color",
        write_only=True,
    )

    bottem_line_color = ColorCRUDSerializer(required=False)
    bottem_line_color_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Color.objects.exclude(is_deleted=True),
        source="bottem_line_color",
        write_only=True,
    )

    collection = CollectionCRUDSerializer(required=False)
    collection_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Collection.objects.exclude(is_deleted=True),
        source="collection",
        write_only=True,
    )

    product = ProductCRUDSerializer(required=False)
    product_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Product.objects.exclude(is_deleted=True),
        source="product",
        write_only=True,
    )

    class Meta:
        model = ProductCollection
        fields = "__all__"
        read_only_fields = (
            "sequence",
            "store",
        )


class CollectionProductSerializer(BaseSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductCollection
        fields = "__all__"
        read_only_fields = ("sequence",)

    def get_product(self, obj):
        if not obj.product:
            return {}
        pass_object = PassObject()
        pass_object._request = self.context.get("request")
        pass_object._store = obj.store
        return AllProductSerializer(obj.product, pass_object=pass_object).data
