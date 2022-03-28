from base.permission import AdminPermission, ModelPermission
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import mixins, viewsets
from v1.delivery.choice import DeliveryBoyStatus
from v1.delivery.models import (
    DeliveryBoy,
    DeliveryBoyDocument,
    DeliveryBoyPayoutInformation,
    DeliveryBoyReview,
    DeliveryBoyVehicleInformation,
    DeliveryBoyVehiclePhotos,
    DeliveryCharges,
)
from v1.delivery.serializers import (
    DeliveryBoyCRUDSerializer,
    DeliveryBoyDocumentCRUDAdminAccessSerializer,
    DeliveryBoyDocumentCRUDSerializer,
    DeliveryBoyPayoutCRUDSerializer,
    DeliveryBoyReviewCRUDSerializer,
    DeliveryBoyVehicleInformationCRUDAdminAccessSerializer,
    DeliveryBoyVehicleInformationCRUDSerializer,
    DeliveryBoyVehiclePhotosCRUDSerializer,
    DeliveryChargesCRUDSerializer,
)
from v1.orders.choice import OrderStatus
from v1.orders.models import Order
from v1.orders.serializers import OrderCRUDSerializer, OrderMutationSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = DeliveryBoy.objects.exclude(is_deleted=True)
    serializer_class = DeliveryBoyCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = ["user", "store", "is_approve", "payout_balance", "status"]
    ordering_fields = ["user", "store", "is_approve", "payout_balance", "status"]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class DeliveryPayoutViewSet(viewsets.ModelViewSet):
    queryset = DeliveryBoyPayoutInformation.objects.exclude(is_deleted=True)
    serializer_class = DeliveryBoyPayoutCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class DeliveryBoyDocumentViewSet(viewsets.ModelViewSet):
    queryset = DeliveryBoyDocument.objects.exclude(is_deleted=True)
    serializer_class = DeliveryBoyDocumentCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]

    def get_serializer_class(self):
        if (
            self.request.user
            and self.request.user.is_authenticated
            and self.request.user.is_superuser
        ):
            return DeliveryBoyDocumentCRUDAdminAccessSerializer
        return self.serializer_class


class DeliveryBoyReviewViewSet(viewsets.ModelViewSet):
    queryset = DeliveryBoyReview.objects.exclude(is_deleted=True)
    serializer_class = DeliveryBoyReviewCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class DeliveryBoyVehiclePhotosViewSet(viewsets.ModelViewSet):
    queryset = DeliveryBoyVehiclePhotos.objects.exclude(is_deleted=True)
    serializer_class = DeliveryBoyVehiclePhotosCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]


class DeliveryBoyVehicleInformationViewSet(viewsets.ModelViewSet):
    queryset = DeliveryBoyVehicleInformation.objects.exclude(is_deleted=True)
    serializer_class = DeliveryBoyVehicleInformationCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]

    def get_serializer_class(self):
        if (
            self.request.user
            and self.request.user.is_authenticated
            and self.request.user.is_superuser
        ):
            return DeliveryBoyVehicleInformationCRUDAdminAccessSerializer
        return self.serializer_class


class DeliveryChargesViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCharges.objects.exclude(is_deleted=True)
    serializer_class = DeliveryChargesCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [AdminPermission]


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
            if self.request.user.is_online:
                try:
                    delivery_boy = DeliveryBoy.objects.get(
                        user=self.request.user, is_approve=True, is_deleted=False
                    )
                    if delivery_boy.current_status in [
                        DeliveryBoyStatus.READY_FOR_ORDER_PICKED_UP,
                        DeliveryBoyStatus.ONLINE,
                    ]:
                        return self.queryset.filter(
                            order_status=OrderStatus.ORDER_PACKING_COMPLETED,
                            store=delivery_boy.store,
                        )
                except Exception:
                    return self.queryset.none()
        return self.queryset.none()

    def get_serializer_class(self):
        if self.action == "partial_update" or self.action == "update":
            return OrderMutationSerializer
        return self.serializer_class
