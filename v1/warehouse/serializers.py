from base.serializers import BaseSerializer, CustomBase64FileField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from v1.catalog.serializers import VariationCRUDSerializer
from v1.store.serializers import StoreExcloudGeoLocationSerializer
from v1.warehouse.tasks import stock_purchase
from v1.catalog.models import Variation

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


class GettingPurchaseMultiItemCRUDSerializer(BaseSerializer):
    id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=PurchaseMultiItem.objects.exclude(is_deleted=True),
    )

    product_and_variation = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Variation.objects.exclude(is_deleted=True),
    )

    class Meta:
        model = PurchaseMultiItem
        fields = [
            "id",
            "product_and_variation",
            "quantity",
            "unit_cost",
            "price",
        ]


class PurchaseCRUDSerializer(BaseSerializer):
    item_supplier_object = serializers.SerializerMethodField(read_only=True)
    warehouse_object = serializers.SerializerMethodField(read_only=True)
    multiple_item_object = serializers.SerializerMethodField(read_only=True)
    multiple_item = GettingPurchaseMultiItemCRUDSerializer(
        required=False, many=True, write_only=True
    )
    attach_document = CustomBase64FileField(required=False)

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
        if not obj.multiple_item.all():
            return []
        return PurchaseMultiItemCRUDSerializer(obj.multiple_item.all(), many=True).data

    def create(self, validated_data):
        multiple_item = validated_data.pop("multiple_item", [])
        purchase = super(PurchaseCRUDSerializer, self).create(validated_data)
        purchase_ids = []
        if multiple_item:
            for item in multiple_item:
                serializer = PurchaseMultiItemCRUDSerializer(data=item)
                if serializer.is_valid(raise_exception=True):
                    save_item = serializer.save()
                    purchase_ids.append(save_item.pk)
            purchase.multiple_item.set(purchase_ids)
            purchase.save()
            stock_purchase.delay(purchase)
        return purchase

    def update(self, instance, validated_data):
        multiple_item = validated_data.pop("multiple_item", [])
        purchase = super(PurchaseCRUDSerializer, self).update(instance, validated_data)
        purchase_ids = []
        if multiple_item:
            for item in multiple_item:
                item_instance = None

                if item.get("id"):
                    item_instance = item.pop("id", None)
                    product_and_variation = item.pop("product_and_variation", None)
                    if product_and_variation:
                        item["product_and_variation"] = product_and_variation

                if item_instance:
                    serializer = PurchaseMultiItemCRUDSerializer(data=item)
                    if serializer.is_valid(raise_exception=True):
                        save_item = serializer.update(
                            instance=item_instance,
                            validated_data=item,
                        )
                        purchase_ids.append(save_item.pk)
                else:
                    serializer = PurchaseMultiItemCRUDSerializer(data=item)
                    if serializer.is_valid(raise_exception=True):
                        save_item = serializer.save()
                        purchase_ids.append(save_item.pk)

            purchase.multiple_item.set(purchase_ids)
            purchase.save()
            stock_purchase.delay(purchase)
        return purchase


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
        return StoreExcloudGeoLocationSerializer(
            obj.multiple_item.all(), many=True
        ).data


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
