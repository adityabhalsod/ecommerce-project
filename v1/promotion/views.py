from constance import config
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from base.permission import AdminPermission, ModelPermission
from base.response import Response
from v1.promotion.models import DiscountVoucher, ReferralAndEarn
from v1.promotion.permission import ReferralAndEarnPermission
from v1.promotion.serializers import (
    DiscountVoucherSerializer,
    ReferralAndEarnSerializer,
)


class DiscountVoucherViewSet(viewsets.ModelViewSet):
    queryset = DiscountVoucher.objects.exclude(is_deleted=True, is_active=False)
    serializer_class = DiscountVoucherSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = [
        "get",
        "head",
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = "__all__"
    permission_classes = [ModelPermission]


class DiscountVoucherMutationViewSet(viewsets.ModelViewSet):
    queryset = DiscountVoucher.objects.exclude(is_deleted=True, is_active=False)
    serializer_class = DiscountVoucherSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = "__all__"
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [AdminPermission]


class ReferralAndEarnViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ReferralAndEarn.objects.exclude(is_deleted=True)
    serializer_class = ReferralAndEarnSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    permission_classes = [ReferralAndEarnPermission]

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            queryset = self.queryset.filter(refer_customer=self.request.user)
            return self.filter_queryset(queryset)
        return self.queryset.none()

    @action(
        detail=False,
        methods=["GET"],
        url_path="earning-price",
    )
    def earning_price(self, request, *args, **kwargs):
        data = {"amount": config.REFER_AND_EARN_PRICE}
        return Response(
            data=data,
            message="Successfully showing the constact data",
            status=status.HTTP_200_OK,
        )
