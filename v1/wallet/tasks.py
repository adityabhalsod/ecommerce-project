from config.celery import app
from django.utils import timezone
from v1.wallet.choice import (
    TransactionMethod,
    TransactionPlatform,
    TransactionStatus,
    TransactionType,
    WalletType,
)
from v1.wallet.models import CustomerWallet, DeliveryBoyWallet, Transaction


def initialization_wallet(instance, wallet_type):
    data = {
        "name": "Initialization wallet.",
        "notes": "Initialization wallet.",
        "transaction_type": TransactionType.NOT_ATTEMPT,
        "method": TransactionMethod.NOT_ATTEMPT,
        "status": TransactionStatus.SUCCESSFUL,
        "platform": TransactionPlatform.WALLET,
        "datetime": timezone.now(),
        "amount": 0.0,
    }
    if wallet_type == WalletType.CUSTOMER:
        data["customer_wallet"] = instance
    elif wallet_type == WalletType.DELIVERY_BOY:
        data["delivery_boy_wallet"] = instance
    return Transaction.objects.create(**data)


def referral_and_earn_wallet(instance, money=0.0):
    customer_wallet, created = CustomerWallet.objects.get_or_create(customer=instance)

    if created:
        instance.balance_amount = 0.0
        instance.is_active = True
        instance.save()
        initialization_wallet(instance=instance, wallet_type=WalletType.CUSTOMER)

    data = {
        "name": "Adding money in wallet using refer and earning.",
        "notes": "Refer and earning amount {}/- Rs. after, complete the first order from refferning customer then automatically add this money into in your wallet.".format(
            money
        ),
        "transaction_type": TransactionType.ADD_MONEY_IN_WALLET,
        "method": TransactionMethod.CREDIT,
        "status": TransactionStatus.WATING,
        "platform": TransactionPlatform.WALLET,
        "datetime": timezone.now(),
        "customer_wallet": customer_wallet,
        "amount": money,
    }
    return Transaction.objects.create(**data)


@app.task
def customer_wallet(customer):
    data = {
        "customer": customer,
    }
    instance, created = CustomerWallet.objects.get_or_create(**data)
    if created:
        instance.balance_amount = 0.0
        instance.is_active = True
        instance.save()
        initialization_wallet(instance=instance, wallet_type=WalletType.CUSTOMER)
    return True


@app.task
def delivery_boy_wallet(delivery_boy):
    data = {
        "delivery_boy": delivery_boy,
    }
    instance, created = DeliveryBoyWallet.objects.get_or_create(**data)
    if created:
        instance.balance_amount = 0.0
        instance.is_active = True
        instance.save()
        initialization_wallet(instance=instance, wallet_type=WalletType.DELIVERY_BOY)
    return True
