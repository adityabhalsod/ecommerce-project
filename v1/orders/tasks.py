import json

from config.celery import app
from django.utils import timezone
from datetime import timedelta
from service.payment.client import PaymentClient
from v1.orders.choice import OrderStatus, OrderType, PaymentStatus
from v1.orders.models import Order
from v1.wallet.choice import (
    TransactionMethod,
    TransactionPlatform,
    TransactionStatus,
    TransactionType,
)
from v1.wallet.models import Transaction


@app.task
def order_payment_creating(paymet_data, order):
    payment_client = PaymentClient()
    response = payment_client.create_order(paymet_data)
    print(":::::Response from payment client\n", response, "\n:::::")
    try:
        order.order_token = response.get("cftoken")
        transaction_data = {
            "name": "{} :: Quickly Order ".format(order.order_number),
            "notes": "Create order by {}".format(order.customer.get_full_name()),
            "transaction_type": TransactionType.PAYMENT,
            "method": TransactionMethod.DEBIT,
            "status": TransactionStatus.WATING,
            "platform": TransactionPlatform.ONLINE,
            "datetime": timezone.now(),
            "payment_payload": json.dumps(response),
            "amount": order.total_amount,
        }
        order_transaction = Transaction.objects.create(**transaction_data)
        order.transaction = order_transaction
        order.save()
    except Exception:
        pass
    return True


@app.task
def order_cash_on_delivery_creating(order):
    try:
        data = {
            "name": "{} :: Quickly Order ".format(order.order_number),
            "notes": "Create order by {}".format(order.customer.get_full_name()),
            "transaction_type": TransactionType.PAYMENT,
            "method": TransactionMethod.DEBIT,
            "status": TransactionStatus.WATING,
            "platform": TransactionPlatform.CASH,
            "datetime": timezone.now(),
            "amount": order.total_amount,
        }
        order_transaction = Transaction.objects.create(**data)
        order.transaction = order_transaction
        order.save()
    except Exception:
        pass
    return True


@app.task
def automatically_order_expired():
    time = timezone.now() - timedelta(minutes=30)
    orders = Order.objects.filter(
        order_status=OrderStatus.ORDER_AWAITING_FOR_PAYMENT,
        order_type=OrderType.ONLINE,
        order_date__lt=time,
    )

    for order in orders:
        order.order_status = OrderStatus.ORDER_CANCEL
        order.payment_status = PaymentStatus.FAILED
        order.save()
    return True
