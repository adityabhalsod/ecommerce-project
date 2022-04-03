from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from base.serializers import BaseSerializer
from v1.catalog.models import Variation
from v1.catalog.serializers import VariationCRUDSerializer

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
    attach_document = Base64FileField(required=False)

    class Meta:
        model = Purchase
        fields = "__all__"


class StockTransferMultiItemCRUDSerializer(BaseSerializer):
    class Meta:
        model = StockTransferMultiItem
        fields = "__all__"


class StockTransferCRUDSerializer(BaseSerializer):
    multiple_item = StockTransferMultiItemCRUDSerializer(required=False)

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
    class Meta:
        model = WarehouseStockManagement
        fields = "__all__"


class StoreStockManagementCRUDSerializer(BaseSerializer):
    class Meta:
        model = StoreStockManagement
        fields = "__all__"
