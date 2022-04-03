from drf_extra_fields.fields import Base64FileField
from rest_framework.exceptions import ValidationError
from base.serializers import BaseSerializer
from v1.catalog.serializers import VariationCRUDSerializer
from v1.store.serializers import StoreExcloudGeoLocationSerializer
from rest_framework import serializers

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
    item_supplier_object = serializers.SerializerMethodField(read_only=True)
    warehouse_object = serializers.SerializerMethodField(read_only=True)
    multiple_item_object = serializers.SerializerMethodField(read_only=True)
    # multiple_item = PurchaseMultiItemCRUDSerializer(required=False)
    attach_document = Base64FileField(required=False)

    class Meta:
        model = Purchase
        fields = "__all__"

    def get_item_supplier_object(self, obj):
        if not obj.item_supplier:
            return {}
        return SupplierCRUDSerializer(obj.item_supplier).data

    def get_warehouse_object(self, obj):
        if not obj.warehouse:
            return {}
        return WarehouseCRUDSerializer(obj.warehouse).data
    
    def get_multiple_item_object(self, obj):
        if not obj.warehouse:
            return []
        return PurchaseMultiItemCRUDSerializer(many=True)


class StockTransferMultiItemCRUDSerializer(BaseSerializer):
    product_and_variation_object = serializers.SerializerMethodField(read_only=True)
    warehouse_object = serializers.SerializerMethodField(read_only=True)
    store_object = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = StockTransferMultiItem
        fields = "__all__"

    def get_product_and_variation_object(self, obj):
        if not obj.product_and_variation:
            return {}
        return VariationCRUDSerializer(obj.product_and_variation).data

    def get_warehouse_object(self, obj):
        if not obj.warehouse:
            return {}
        return WarehouseCRUDSerializer(obj.warehouse).data

    def get_store_object(self, obj):
        if not obj.multiple_item.all():
            return []
        return StoreExcloudGeoLocationSerializer(obj.multiple_item.all(), many=True).data

   

class StockTransferCRUDSerializer(BaseSerializer):
    # multiple_item = StockTransferMultiItemCRUDSerializer(required=False)
    store_object = StoreExcloudGeoLocationSerializer(read_only=True)
    product_and_variation_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StockTransfer
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get("store") and attrs.get("warehouse"):
            store = attrs.get("store")
            if store.warehouse != attrs.get("warehouse"):
                raise ValidationError(
                    {"store_id": "Select store to not found this warehouse."}
                )
        return attrs

    def get_store_object(self, obj):
        if not obj.store:
            return {}
        return StoreExcloudGeoLocationSerializer(obj.store).data

    def get_product_and_variation_object(self, obj):
        if not obj.product_and_variation:
            return {}
        return VariationCRUDSerializer(obj.product_and_variation).data


class WarehouseStockManagementCRUDSerializer(BaseSerializer):
    product_and_variation_object = serializers.SerializerMethodField(read_only=True)
    warehouse_object = serializers.SerializerMethodField(read_only=True)
    purchase_reference_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WarehouseStockManagement
        fields = "__all__"

    def get_product_and_variation_object(self, obj):
        if not obj.product_and_variation:
            return {}
        return VariationCRUDSerializer(obj.product_and_variation).data

    def get_warehouse_object(self, obj):
        if not obj.warehouse:
            return {}
        return WarehouseCRUDSerializer(obj.warehouse).data

    def get_purchase_reference_object(self, obj):
        if not obj.purchase_reference:
            return {}
        return PurchaseCRUDSerializer(obj.purchase_reference).data


class StoreStockManagementCRUDSerializer(BaseSerializer):
    product_and_variation_object = serializers.SerializerMethodField(read_only=True)
    store_object = serializers.SerializerMethodField(read_only=True)
    transfer_reference_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StoreStockManagement
        fields = "__all__"

    def get_product_and_variation_object(self, obj):
        if not obj.product_and_variation:
            return {}
        return VariationCRUDSerializer(obj.product_and_variation).data

    def get_store_object(self, obj):
        if not obj.store:
            return {}
        return StoreExcloudGeoLocationSerializer(obj.store).data

    def get_transfer_reference_object(self, obj):
        if not obj.transfer_reference:
            return {}
        return StockTransferCRUDSerializer(obj.transfer_reference).data
