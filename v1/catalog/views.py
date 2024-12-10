from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import status, viewsets, mixins
from rest_framework.exceptions import ValidationError
from base.permission import ModelPermission
from base.response import Response
from v1.catalog.models import (
    Category,
    Product,
    ProductPhoto,
    ProductStockMaster,
    Unit,
    VariationPhoto,
)
from v1.catalog.serializers import (
    AllProductSearchSerializer,
    CategoryCRUDSerializer,
    ProductCRUDSerializer,
    ProductPhotoCRUDSerializer,
    ProductStockMasterCRUDSerializer,
    ProductStockMasterReadOnlySerializer,
    UnitCRUDSerializer,
    VariationPhotoCRUDSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.exclude(is_deleted=True)
    serializer_class = CategoryCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = [
        "name",
        "parent_category",
        "sequence",
        "is_main",
        "description",
    ]
    ordering_fields = [
        "name",
        "product_count",
        "sequence",
        "is_main",
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, "product_count") and instance.product_count > 0:
            raise ValidationError(
                {"product_count": "In this category to exists some products."}
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.exclude(is_deleted=True)
    serializer_class = ProductCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class ProductPhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductPhoto.objects.exclude(is_deleted=True)
    serializer_class = ProductPhotoCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class ProductStockMasterViewSet(viewsets.ModelViewSet):
    queryset = ProductStockMaster.objects.exclude(is_deleted=True)
    serializer_class = ProductStockMasterCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]
    search_fields = [
        "product__item_name",
        "product__bill_display_item_name",
        "product__short_description",
        "product__search_keyword",
        "product__slug",
        "stock_master_variation__name",
        "stock_master_variation__value",
    ]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductStockMasterReadOnlySerializer
        return self.serializer_class


class ProductSearchViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Product.objects.exclude(is_deleted=True)
    serializer_class = AllProductSearchSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = [
        "get",
        "head",
    ]
    permission_classes = [ModelPermission]
    search_fields = [
        "item_name",
        "bill_display_item_name",
        "short_description",
        "search_keyword",
        "slug",
    ]


class VariationPhotoViewSet(viewsets.ModelViewSet):
    queryset = VariationPhoto.objects.exclude(is_deleted=True)
    serializer_class = VariationPhotoCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.exclude(is_deleted=True)
    serializer_class = UnitCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.product_unit and instance.product_unit.all():
            raise ValidationError(
                {"product_unit": "In unit to exists in some products."}
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
