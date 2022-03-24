from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets
from base.permission import ModelPermission
from v1.group.serializers import (
    CollectionCRUDSerializer,
    CollectionProductSerializer,
    ColorCRUDSerializer,
    GroupStructureAdminCRUDSerializer,
    GroupStructureCRUDSerializer,
    GroupTypeCRUDSerializer,
    MultiplePhotosCRUDSerializer,
    ProductCollectionCRUDSerializer,
)

from .models import (
    Collection,
    Color,
    GroupStructure,
    GroupType,
    MultiplePhotos,
    ProductCollection,
)


class GroupTypeViewSet(viewsets.ModelViewSet):
    queryset = GroupType.objects.exclude(is_deleted=True)
    serializer_class = GroupTypeCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.exclude(is_deleted=True)
    serializer_class = ColorCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class GroupStructureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GroupStructure.objects.filter(is_main=True).exclude(is_deleted=True)
    serializer_class = GroupStructureCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = [
        "store",
        "group_name",
        "sequence",
        "is_active",
        "parent_group",
        "level",
        "self_identify",
        "short_text",
    ]
    ordering_fields = [
        "store",
        "group_name",
        "sequence",
        "is_active",
        "parent_group",
        "level",
        "self_identify",
        "short_text",
    ]
    search_fields = [
        "store",
        "group_name",
        "sequence",
        "is_active",
        "parent_group",
        "level",
        "self_identify",
        "short_text",
        "is_main",
    ]
    permission_classes = [ModelPermission]


class GroupStructureAdminViewSet(viewsets.ModelViewSet):
    queryset = GroupStructure.objects.exclude(is_deleted=True)
    serializer_class = GroupStructureAdminCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = [
        "store",
        "group_name",
        "sequence",
        "is_active",
        "parent_group",
        "level",
        "self_identify",
        "short_text",
        "is_main",
    ]
    ordering_fields = [
        "store",
        "group_name",
        "sequence",
        "is_active",
        "parent_group",
        "level",
        "self_identify",
        "short_text",
        "is_main",
    ]
    search_fields = [
        "store",
        "group_name",
        "sequence",
        "is_active",
        "parent_group",
        "level",
        "self_identify",
        "short_text",
        "is_main",
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class MultiplePhotosViewSet(viewsets.ModelViewSet):
    queryset = MultiplePhotos.objects.exclude(is_deleted=True)
    serializer_class = MultiplePhotosCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.exclude(is_deleted=True)
    serializer_class = CollectionCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class ProductCollectionViewSet(viewsets.ModelViewSet):
    queryset = ProductCollection.objects.exclude(is_deleted=True)
    serializer_class = ProductCollectionCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = ["store","product","product__category"]
    ordering_fields = "__all__"
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]

    def get_serializer_class(self):
        if self.action in ["list", "detail", "retrieve"]:
            return CollectionProductSerializer
        return self.serializer_class
