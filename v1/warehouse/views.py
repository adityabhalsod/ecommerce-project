from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets
from base.permission import ModelPermission
from v1.warehouse.serializers import (
    PurchaseCRUDSerializer,
    StockTransferCRUDSerializer,
    StoreStockManagementCRUDSerializer,
    SupplierCRUDSerializer,
    WarehouseCRUDSerializer,
    WarehouseStockManagementCRUDSerializer,
)
from v1.warehouse.models import (
    Purchase,
    StockTransfer,
    StoreStockManagement,
    Supplier,
    Warehouse,
    WarehouseStockManagement,
)


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.exclude(is_deleted=True)
    serializer_class = PurchaseCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = [
        "multiple_item",
        "item_supplier",
        "reference_number",
        "datetime",
        "warehouse",
        "total_items",
        "sub_total",
        "additional_shipping_charges",
        "additional_notes",
        "discount_type",
        "tax",
        "discount",
        "purchase_total",
    ]
    ordering_fields = [
        "multiple_item",
        "item_supplier",
        "reference_number",
        "datetime",
        "warehouse",
        "total_items",
        "sub_total",
        "additional_shipping_charges",
        "additional_notes",
        "discount_type",
        "tax",
        "discount",
        "purchase_total",
    ]
    search_fields = [
        "multiple_item",
        "item_supplier",
        "reference_number",
        "datetime",
        "warehouse",
        "total_items",
        "sub_total",
        "additional_shipping_charges",
        "additional_notes",
        "discount_type",
        "tax",
        "discount",
        "purchase_total",
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.exclude(is_deleted=True)
    serializer_class = StockTransferCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = "__all__"
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.exclude(is_deleted=True)
    serializer_class = WarehouseCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = "__all__"
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.exclude(is_deleted=True)
    serializer_class = SupplierCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = "__all__"
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class WarehouseStockManagementViewSet(viewsets.ModelViewSet):
    queryset = WarehouseStockManagement.objects.exclude(is_deleted=True)
    serializer_class = WarehouseStockManagementCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = "__all__"
    http_method_names = [
        "get",
        "head",
    ]
    permission_classes = [ModelPermission]


class StoreStockManagementViewSet(viewsets.ModelViewSet):
    queryset = StoreStockManagement.objects.exclude(is_deleted=True)
    serializer_class = StoreStockManagementCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = "__all__"
    http_method_names = [
        "get",
        "head",
    ]
    permission_classes = [ModelPermission]
