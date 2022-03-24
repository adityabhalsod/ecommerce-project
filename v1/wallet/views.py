import json
from base.permission import ModelPermission
from base.response import Response
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet
from v1.wallet.choice import (
    TransactionMethod,
    TransactionPlatform,
    TransactionStatus,
    TransactionType,
    WalletType,
)
from v1.wallet.models import (
    CaseOnDeliveryCollectionHistory,
    CustomerWallet,
    DeliveryBoyWallet,
    Transaction,
)
from v1.wallet.serializers import (
    AddingMoneySerializer,
    CaseOnDeliveryCollectionHistoryCRUDSerializer,
    CustomerWalletCRUDSerializer,
    DeliveryBoyWalletCRUDSerializer,
    TransactionCRUDSerializer,
)
from v1.wallet.tasks import initialization_wallet
from service.payment.client import PaymentClient


class CustomerWalletViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = CustomerWallet.objects.exclude(is_deleted=True)
    serializer_class = CustomerWalletCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    permission_classes = [ModelPermission]

    def get_serializer_class(self):
        if self.action == "add_money":
            return AddingMoneySerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=["POST"],
        url_path="add-money",
    )
    def add_money(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        validate_data = {}
        payment_token = ""
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError(
                {"message": "Transaction are not create invalid data!."}
            )

        validate_data = serializer.validated_data
        if validate_data.get("balance_amount") <= 0:
            raise ValidationError({"balance_amount": "Minimum adding 1 Rs."})

        customer_wallet, created = CustomerWallet.objects.get_or_create(
            customer=request.user
        )
        if created:
            customer_wallet.balance_amount = 0.0
            customer_wallet.is_active = True
            customer_wallet.save()
            initialization_wallet(
                instance=customer_wallet, wallet_type=WalletType.CUSTOMER
            )

        transaction_data = {
            "name": "{} have adding money in wallet.".format(
                customer_wallet.customer.get_full_name()
            ),
            "notes": "Amount {}/- Rs. after, complete the payment then automatically add this money into in your wallet.".format(
                validate_data.get("balance_amount")
            ),
            "transaction_type": TransactionType.ADD_MONEY_IN_WALLET,
            "method": TransactionMethod.CREDIT,
            "status": TransactionStatus.WATING,
            "platform": TransactionPlatform.WALLET,
            "datetime": timezone.now(),
            "customer_wallet": customer_wallet,
            "amount": validate_data.get("balance_amount"),
        }
        transaction = Transaction.objects.create(**transaction_data)
        transaction.refresh_from_db()

        ##### Create payment
        paymet_data = {
            "orderId": str(transaction.reference),
            "orderAmount": transaction.amount,
            "orderCurrency": "INR",
        }
        payment_client = PaymentClient()
        payment_response = payment_client.create_order(paymet_data)
        payment_token = payment_response.get("cftoken", "")
        ##### Create payment

        ##### adding money payment payload save
        transaction.payment_payload = json.dumps(payment_response)
        transaction.save()
        ##### adding money payment payload save

        response_data = {
            "balance_amount": validate_data.get("balance_amount"),
            "reference": str(transaction.reference),
            "payment_token": str(payment_token),
        }

        return Response(
            data=response_data,
            message="Successfully create transaction.",
            status=status.HTTP_200_OK,
        )


class DeliveryBoyWalletViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = DeliveryBoyWallet.objects.exclude(is_deleted=True)
    serializer_class = DeliveryBoyWalletCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    permission_classes = [ModelPermission]


class TransactionViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Transaction.objects.exclude(is_deleted=True)
    serializer_class = TransactionCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    permission_classes = [ModelPermission]


class CaseOnDeliveryCollectionHistoryViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = CaseOnDeliveryCollectionHistory.objects.exclude(is_deleted=True)
    serializer_class = CaseOnDeliveryCollectionHistoryCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    permission_classes = [ModelPermission]
