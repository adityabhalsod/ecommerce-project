import base64
import json

from constance import config
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from base.response import Response
from v1.orders.choice import OrderStatus, PaymentStatus
from v1.orders.models import Order
from v1.wallet.choice import TransactionStatus
from v1.wallet.models import Transaction


class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=["GET"],
        url_path="secret-key",
    )
    def secret_key(self, request, *args, **kwargs):
        if config.IS_ACTIVE_LIVE_ENVIRONMENT:
            URL = "https://api.cashfree.com/"
            ID = config.PAYMENT_APP_ID_LIVE
            SECRET_KEY = config.PAYMENT_SECRET_KEY_LIVE
            ENV = "PROD"
        else:
            URL = "https://test.cashfree.com/"
            ID = config.PAYMENT_APP_ID_TEST
            SECRET_KEY = config.PAYMENT_SECRET_KEY_TEST
            ENV = "TEST"

        data = {
            "URL": URL,
            "PAYMENT_APP_ID": ID,
            "PAYMENT_SECRET_KEY": SECRET_KEY,
            "ENVIRONMENT": ENV,
        }

        data = json.dumps(data)
        return Response(
            data={"config": base64.b64encode(data.encode("utf-8"))},
            message="Successfully showing the constact data",
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["POST"],
        url_path="webhook",
    )
    def webhook(self, request, *args, **kwargs):
        order_id = request.POST.get("orderId", "")
        status = request.POST.get("txStatus", "")

        if status == "FAILED":
            if str(order_id).startswith("Q"):
                try:
                    order = Order.objects.get(order_number=order_id)
                except Exception:
                    order = None

                if order:
                    order.order_status = OrderStatus.ORDER_FAILED
                    order.payment_status = PaymentStatus.FAILED
                    order.save()

                    try:
                        transaction = Transaction.objects.get(pk=order.transaction.pk)
                        transaction.payment_response = str(request.POST)
                        transaction.status = TransactionStatus.FAILED
                        transaction.save()
                    except Exception:
                        pass

            elif str(order_id).startswith("TXT"):
                try:
                    transaction = Transaction.objects.get(reference=order_id)
                    transaction.payment_response = json.dumps(request.POST)
                    transaction.status = TransactionStatus.FAILED
                    transaction.save()
                except Exception:
                    pass

        if request.data and isinstance(request.data, dict):
            if request.data.get("type") == "PAYMENT_SUCCESS_WEBHOOK":
                order_id = request.data.get("data", {}).get("order", {}).get("order_id")
                if order_id and isinstance(order_id, str):
                    if order_id.startswith("Q"):
                        try:
                            order = Order.objects.get(order_number=order_id)
                        except Exception:
                            order = None

                        if order:
                            order.order_status = OrderStatus.ORDER_PLACED
                            order.payment_status = PaymentStatus.SUCCESSFUL
                            order.save()

                            try:
                                transaction = Transaction.objects.get(
                                    pk=order.transaction.pk
                                )
                                transaction.payment_response = json.dumps(request.data)
                                transaction.status = TransactionStatus.SUCCESSFUL
                                transaction.save()
                            except Exception:
                                pass

                    elif order_id.startswith("TXT"):
                        try:
                            transaction = Transaction.objects.get(reference=order_id)
                            transaction.payment_response = json.dumps(request.data)
                            transaction.status = TransactionStatus.SUCCESSFUL
                            transaction.save()
                        except Exception:
                            pass

        return Response(
            data={},
            message="Successfully call the webhook.",
            status=status.HTTP_200_OK,
        )
