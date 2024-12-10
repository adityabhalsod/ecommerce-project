from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from base.serializers import BaseSerializer, PassObject
from v1.store.models import Store
from v1.store.serializers import StoreExcloudGeoLocationSerializer

from .models import (
    Category,
    Product,
    ProductPhoto,
    ProductStockMaster,
    Unit,
    Variation,
    VariationPhoto,
)


class CategoryCRUDSerializer(BaseSerializer):
    image = Base64ImageField(required=False)
    parent_category = serializers.SerializerMethodField(read_only=True)
    main_category_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Category.objects.exclude(is_deleted=True),
        source="parent_category",
        write_only=True,
    )
    product_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = (
            "slug",
            "is_main",
        )

    def get_product_count(self, obj):
        if not hasattr(obj, "product_count"):
            return 0
        return obj.product_count

    def get_parent_category(self, obj):
        sub_category = obj.children.exclude(is_deleted=True)
        if not sub_category:
            return []
        return CategoryCRUDSerializer(
            sub_category, many=True, context={"request": self.context.get("request")}
        ).data

    def update(self, instance, validated_data):
        if instance.parent_category and instance.parent_category.pk == instance.pk:
            raise ValidationError(
                {
                    "main_category_id": "Not able to set the parent category as a this category."
                }
            )

        if (
            instance.parent_category
            and instance.parent_category.parent_category
            and instance.parent_category.parent_category.pk == instance.pk
        ):
            raise ValidationError(
                {"main_category_id": "Not able to set the recursive category."}
            )
        instance = super(CategoryCRUDSerializer, self).update(instance, validated_data)
        return instance


class ProductPhotoCRUDSerializer(BaseSerializer):
    original = Base64ImageField(required=False)

    class Meta:
        model = ProductPhoto
        fields = "__all__"


class UnitCRUDSerializer(BaseSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class ProductCRUDSerializer(BaseSerializer):
    photos = ProductPhotoCRUDSerializer(read_only=True, many=True)
    photo_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=ProductPhoto.objects.exclude(is_deleted=True),
        source="photos",
        write_only=True,
        many=True,
    )

    category = CategoryCRUDSerializer(required=False)
    category_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Category.objects.exclude(is_deleted=True),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("slug",)


class VariationPhotoCRUDSerializer(BaseSerializer):
    original = Base64ImageField(required=False)

    class Meta:
        model = VariationPhoto
        fields = "__all__"


class VariationGettingTimeSerializer(BaseSerializer):
    id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Variation.objects.exclude(is_deleted=True),
    )
    photos = VariationPhotoCRUDSerializer(read_only=True, many=True)
    photo_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=VariationPhoto.objects.exclude(is_deleted=True),
        source="photos",
        write_only=True,
        many=True,
    )
    unit = UnitCRUDSerializer(required=False, read_only=True)

    class Meta:
        model = Variation
        fields = "__all__"


class VariationReadOnlySerializer(BaseSerializer):
    photos = VariationPhotoCRUDSerializer(read_only=True, many=True)
    unit = UnitCRUDSerializer(required=False, read_only=True)
    position = serializers.SerializerMethodField(read_only=True)
    row = serializers.SerializerMethodField(read_only=True)
    rack = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Variation
        fields = "__all__"

    def get_position(self, obj):
        if obj.product_stock_master and obj.product_stock_master.position:
            return str(obj.product_stock_master.position)
        return ""

    def get_row(self, obj):
        if obj.product_stock_master and obj.product_stock_master.row:
            return str(obj.product_stock_master.row)
        return ""

    def get_rack(self, obj):
        if obj.product_stock_master and obj.product_stock_master.rack:
            return str(obj.product_stock_master.rack)
        return ""


class VariationCRUDSerializer(BaseSerializer):
    photos = VariationPhotoCRUDSerializer(read_only=True, many=True)
    photo_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=VariationPhoto.objects.exclude(is_deleted=True),
        source="photos",
        write_only=True,
        many=True,
    )

    unit = UnitCRUDSerializer(required=False)
    unit_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Unit.objects.exclude(is_deleted=True),
        source="unit",
        write_only=True,
    )

    class Meta:
        model = Variation
        fields = "__all__"

    def validate(self, attrs):
        if self.context.get("product_stock_master"):
            attrs["product_stock_master"] = self.context.get("product_stock_master")
        return attrs


class ProductStockMasterCRUDSerializer(BaseSerializer):
    store = StoreExcloudGeoLocationSerializer(read_only=True, many=True)
    store_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        many=True,
        write_only=True,
    )
    product = ProductCRUDSerializer(read_only=True, required=False)
    product_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Product.objects.exclude(is_deleted=True),
        source="product",
        write_only=True,
    )

    variation = VariationGettingTimeSerializer(required=False, many=True)
    variation_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductStockMaster
        fields = "__all__"

    def create(self, validated_data):
        variation = validated_data.pop("variation", [])
        product_stock_master = super(ProductStockMasterCRUDSerializer, self).create(
            validated_data
        )
        for item in variation:
            if item.get("photos", []):
                item["photo_ids"] = [
                    item and item.pk for item in item.get("photos", [])
                ]
            else:
                item["photo_ids"] = []

            serializer = VariationCRUDSerializer(
                data=item,
                context={"product_stock_master": product_stock_master},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return product_stock_master

    def update(self, instance, validated_data):
        variation = validated_data.pop("variation", [])
        product_stock_master = super(ProductStockMasterCRUDSerializer, self).update(
            instance, validated_data
        )
        for item in variation:
            variation_instance = None
            if item.get("id"):
                variation_instance = item.pop("id")

            if item.get("photos", []):
                item["photo_ids"] = [
                    item and item.pk for item in item.get("photos", [])
                ]
            else:
                item["photo_ids"] = []

            # if not found instance then create new one
            if not variation_instance:
                serializer = VariationCRUDSerializer(
                    data=item,
                    context={"product_stock_master": product_stock_master},
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            else:
                serializer = VariationCRUDSerializer(
                    instance=variation_instance,
                    data=item,
                    context={"product_stock_master": product_stock_master},
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.update(
                        instance=variation_instance,
                        validated_data=item,
                    )
        return product_stock_master

    def get_variation_list(self, obj):
        pass_object = PassObject()
        pass_object._request = self.context.get("request")
        if (
            hasattr(obj, "stock_master_variation")
            and obj.stock_master_variation
            and obj.stock_master_variation.all()
        ):
            return VariationSerializer(
                obj.stock_master_variation.all(), many=True, pass_object=pass_object
            ).data
        return []


class AllProductSerializer(BaseSerializer):
    photos = serializers.SerializerMethodField(read_only=True)
    product_master = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("slug",)

    def get_product_master(self, obj):
        if self.pass_object._store and obj:
            data = ProductStockMaster.objects.filter(
                store=self.pass_object._store,
                product=obj,
            ).first()

            return AllProductVariationSerializer(
                data, pass_object=self.pass_object
            ).data
        return {}

    def get_photos(self, obj):
        if obj.photos:
            return ProductPhotoCRUDSerializer(
                obj.photos,
                read_only=True,
                many=True,
                context={"request": self.pass_object._request},
            ).data
        return {}


class VariationSerializer(BaseSerializer):
    our_rate_difference = serializers.ReadOnlyField(read_only=True)
    member_rate_difference = serializers.ReadOnlyField(read_only=True)
    exclusive_rate_difference = serializers.ReadOnlyField(read_only=True)
    photos = serializers.SerializerMethodField(read_only=True)
    unit = UnitCRUDSerializer(required=False, read_only=True)

    class Meta:
        model = Variation
        exclude = ("product_stock_master",)

    def get_photos(self, obj):
        if obj.photos:
            return VariationPhotoCRUDSerializer(
                obj.photos,
                read_only=True,
                many=True,
                context={"request": self.pass_object._request},
            ).data
        return {}


class AllProductVariationSerializer(BaseSerializer):
    variation = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductStockMaster
        fields = "__all__"

    def get_variation(self, obj):
        return VariationSerializer(
            obj.stock_master_variation, many=True, pass_object=self.pass_object
        ).data


class ProductStockMasterReadOnlySerializer(BaseSerializer):
    store = StoreExcloudGeoLocationSerializer(read_only=True, many=True)
    product = ProductCRUDSerializer(read_only=True)
    variation = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductStockMaster
        fields = "__all__"

    def get_variation(self, obj):
        pass_object = PassObject()
        pass_object._request = self.context.get("request")
        if (
            hasattr(obj, "stock_master_variation")
            and obj.stock_master_variation
            and obj.stock_master_variation.all()
        ):
            return VariationSerializer(
                obj.stock_master_variation.all(), many=True, pass_object=pass_object
            ).data
        return []


class AllProductSearchSerializer(BaseSerializer):
    photos = serializers.SerializerMethodField(read_only=True)
    product_master = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("slug",)

    def get_product_master(self, obj):
        pass_object = PassObject()
        pass_object._request = self.context.get("request")

        # search the product store wise.
        search_query = Q()
        request = self.context.get("request")
        if request and request.query_params:
            store_id = request.query_params.get("store_id", 0)
            if store_id:
                search_query.add(Q(store__pk=store_id), Q.AND)

        if obj:
            data = ProductStockMaster.objects.filter(
                search_query,
                product=obj,
            ).first()

            return AllProductVariationSerializer(data, pass_object=pass_object).data
        return {}

    def get_photos(self, obj):
        if obj.photos:
            return ProductPhotoCRUDSerializer(
                obj.photos,
                read_only=True,
                many=True,
                context={"request": self.context.get("request")},
            ).data
        return {}
