from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from base.serializers import BaseSerializer

from .models import (
    CaseOnDeliveryCollectionHistory,
    CustomerWallet,
    DeliveryBoyWallet,
    Transaction,
)


class CustomerWalletCRUDSerializer(BaseSerializer):
    class Meta:
        model = CustomerWallet
        fields = "__all__"


class DeliveryBoyWalletCRUDSerializer(BaseSerializer):
    class Meta:
        model = DeliveryBoyWallet
        fields = "__all__"


class TransactionCRUDSerializer(BaseSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CaseOnDeliveryCollectionHistoryCRUDSerializer(BaseSerializer):
    class Meta:
        model = CaseOnDeliveryCollectionHistory
        fields = "__all__"


class AddingMoneySerializer(BaseSerializer):
    class Meta:
        model = CustomerWallet
        fields = ("balance_amount",)
