from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from base.serializers import BaseSerializer
from v1.catalog.models import Variation
from v1.catalog.serializers import VariationCRUDSerializer
from v1.store.models import Store
from v1.store.serializers import StoreExcloudGeoLocationSerializer

from .models import (
    Purchase,
    PurchaseMultiItem,
    StockTransfer,
    StockTransferMultiItem,
    StoreStockManagement,
    Supplier,
    Warehouse,
    WarehouseStockManagement,
)


class WarehouseCRUDSerializer(BaseSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class SupplierCRUDSerializer(BaseSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class PurchaseMultiItemCRUDSerializer(BaseSerializer):
    class Meta:
        model = PurchaseMultiItem
        fields = "__all__"


class PurchaseCRUDSerializer(BaseSerializer):
    multiple_item = PurchaseMultiItemCRUDSerializer(required=False, many=True)
    multiple_item_ids = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field="id",
        queryset=PurchaseMultiItem.objects.exclude(is_deleted=True),
        source="multiple_item",
        write_only=True,
    )

    item_supplier = SupplierCRUDSerializer(required=False)
    item_supplier_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Supplier.objects.exclude(is_deleted=True),
        source="item_supplier",
        write_only=True,
    )

    warehouse = WarehouseCRUDSerializer(required=False)
    warehouse_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Warehouse.objects.exclude(is_deleted=True),
        source="warehouse",
        write_only=True,
    )

    attach_document = Base64FileField(required=False)

    class Meta:
        model = Purchase
        fields = "__all__"


class StockTransferMultiItemCRUDSerializer(BaseSerializer):
    product_and_variation = VariationCRUDSerializer(read_only=True, required=False)
    product_and_variation_id = serializers.SlugRelatedField(
        required=True,
        slug_field="id",
        queryset=Variation.objects.exclude(is_deleted=True),
        source="product_and_variation",
        write_only=True,
    )

    class Meta:
        model = StockTransferMultiItem
        fields = "__all__"


class StockTransferCRUDSerializer(BaseSerializer):
    multiple_item = StockTransferMultiItemCRUDSerializer(required=False)
    multiple_item_ids = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field="id",
        queryset=StockTransferMultiItem.objects.exclude(is_deleted=True),
        source="multiple_item",
        write_only=True,
    )
    warehouse = WarehouseCRUDSerializer(required=False)
    warehouse_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Warehouse.objects.exclude(is_deleted=True),
        source="warehouse",
        write_only=True,
    )
    store = StoreExcloudGeoLocationSerializer(read_only=True)
    store_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        write_only=True,
    )

    def validate(self, attrs):
        if attrs.get("store") and attrs.get("warehouse"):
            store = attrs.get("store")
            if store.warehouse != attrs.get("warehouse"):
                raise ValidationError(
                    {"store_id": "Select store to not found this warehouse."}
                )
        return attrs

    class Meta:
        model = StockTransfer
        fields = "__all__"


class WarehouseStockManagementCRUDSerializer(BaseSerializer):
    warehouse = WarehouseCRUDSerializer(read_only=True, required=False)
    product_and_variation = VariationCRUDSerializer(read_only=True, required=False)

    class Meta:
        model = WarehouseStockManagement
        fields = "__all__"


class StoreStockManagementCRUDSerializer(BaseSerializer):
    store = StoreExcloudGeoLocationSerializer(read_only=True, required=False)
    product_and_variation = VariationCRUDSerializer(read_only=True, required=False)

    class Meta:
        model = StoreStockManagement
        fields = "__all__"
