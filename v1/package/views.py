from base.permission import ModelPermission
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import mixins, viewsets
from v1.orders.choice import OrderStatus
from v1.orders.models import Order
from v1.orders.serializers import OrderCRUDSerializer, OrderMutationSerializer
from v1.package.models import PackageBoy
from v1.package.serializers import PackageBoy, PackageBoyCRUDSerializer


class PackageBoyViewSet(viewsets.ModelViewSet):
    queryset = PackageBoy.objects.exclude(is_deleted=True)
    serializer_class = PackageBoyCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    permission_classes = [ModelPermission]


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

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            if self.request.user:
                try:
                    package_boy = PackageBoy.objects.get(
                        user=self.request.user, is_approve=True, is_deleted=False
                    )
                    return self.queryset.filter(
                        order_status=OrderStatus.ORDER_PLACED, store=package_boy.store
                    )
                except Exception:
                    return self.queryset.none()
        return self.queryset.none()

    def get_serializer_class(self):
        if self.action == "partial_update" or self.action == "update":
            return OrderMutationSerializer
        return self.serializer_class
