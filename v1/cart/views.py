from distutils.util import strtobool

from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from account.choice import SystemDefaultGroup
from base.permission import ModelPermission
from base.response import Response
from v1.cart.calculation import cart_calculation
from v1.cart.models import Cart, Checkout
from v1.cart.serializers import CartCRUDSerializer, CheckoutCRUDSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.exclude(is_deleted=True)
    serializer_class = CartCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            queryset = self.queryset.filter(customer=self.request.user)
            return self.filter_queryset(queryset)
        return self.queryset.none()

    @action(
        detail=False,
        methods=["POST"],
    )
    def clear(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            customer = request.user
            Cart.objects.filter(customer=customer).exclude(is_deleted=True).delete()
            response = Response(
                data={},
                message="Cart now is empty!.",
                status=status.HTTP_200_OK,
            )
            return response

        response = Response(
            data={},
            message="Customer are not found.",
            status=status.HTTP_401_UNAUTHORIZED,
        )
        return response

    @action(
        detail=False,
        methods=["GET"],
        url_path="billing-info",
    )
    def billing_info(self, request, *args, **kwargs):
        new_membership_adding = request.query_params.get("new_membership_adding", False)
        voucher_pk = request.query_params.get("voucher_id", None)

        if new_membership_adding is None:
            new_membership_adding = False
        else:
            new_membership_adding = strtobool(str(new_membership_adding))

        if not request.user:
            raise ValidationError(
                {"customer": "Customer are not found on current request."}
            )

        if request.user and request.user.is_authenticated:
            customer = request.user
            if not customer.groups.filter(name=SystemDefaultGroup.CUSTOMER).exists():
                raise ValidationError({"customer": "User is not customer."})

            final_data = cart_calculation(
                customer,
                new_membership_adding=new_membership_adding,
                voucher_pk=voucher_pk,
            )
            response = Response(
                data=final_data,
                message="Cart billing information.",
                status=status.HTTP_200_OK,
            )
            return response

        response = Response(
            data={},
            message="Customer are not found.",
            status=status.HTTP_401_UNAUTHORIZED,
        )
        return response


class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.exclude(is_deleted=True)
    serializer_class = CheckoutCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    http_method_names = [
        "post",
        "head",
    ]
    permission_classes = [ModelPermission]

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            queryset = self.queryset.filter(customer=self.request.user)
            return self.filter_queryset(queryset)
        return self.queryset.none()
