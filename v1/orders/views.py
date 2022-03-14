from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import mixins, viewsets
from base.permission import ModelPermission
from v1.orders.models import Order
from v1.orders.serializers import OrderCRUDSerializer, OrderMutationSerializer


class OrderViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.exclude(is_deleted=True)
    serializer_class = OrderCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    http_method_names = [
        "get",
        "patch",
    ]
    permission_classes = [ModelPermission]

    def get_serializer_class(self):
        if self.action == "partial_update" or self.action == "update":
            return OrderMutationSerializer
        return self.serializer_class
