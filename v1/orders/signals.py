from django.db.models.signals import post_save
from django.dispatch import receiver
from v1.membership.calculation import set_membership
from v1.membership.choice import MembershipTypeChoices
from v1.orders.choice import OrderStatus, OrderType, PaymentStatus
from v1.orders.models import Order
from v1.promotion.models import ReferralAndEarn
from v1.wallet.choice import TransactionStatus
from v1.wallet.models import (
    CaseOnDeliveryCollectionHistory,
    CustomerWallet,
    DeliveryBoyWallet,
    Transaction,
)
from v1.wallet.tasks import delivery_boy_wallet


@receiver(post_save, sender=Order)
def order_placed_membership_create(sender, instance, created, **kwargs):
    if instance:
        if (
            instance.payment_status == PaymentStatus.SUCCESSFUL
            and instance.membership_type != MembershipTypeChoices.NOT_ATTEMPT
        ):
            if instance.order_type == OrderType.CASH_ON_DELIVERY:
                is_payment_in_cash = True
            elif instance.order_type == OrderType.ONLINE:
                is_payment_in_cash = False

            set_membership(
                instance.customer,
                instance.membership_type,
                is_payment_done=True,
                is_payment_in_cash=is_payment_in_cash,
            )

        ##### order delivered #####
        if instance.order_status == OrderStatus.ORDER_DELIVERED:
            if (
                instance.order_type == OrderType.CASH_ON_DELIVERY
                and instance.delivery_boy
            ):
                delivery_boy = instance.delivery_boy
                db_amount = instance.collect_amount
                delivery_boy_wallet.delay(instance.delivery_boy)

                try:
                    # delivery boy wallet save
                    db_wallet = DeliveryBoyWallet.objects.get(delivery_boy=delivery_boy)
                    db_wallet.balance_amount = float(db_wallet.balance_amount) + float(
                        db_amount
                    )
                    db_wallet.save()

                    # add history in collection
                    history_data = {
                        "name": "{} - {} /- Rs.".format(
                            instance.order_number, db_amount
                        ),
                        "notes": "{} order to {} /- Rs. amount are collect".format(
                            instance.order_number, db_amount
                        ),
                        "delivery_boy_wallet": db_wallet,
                        "order": instance,
                        "amount": float(db_amount),
                    }
                    CaseOnDeliveryCollectionHistory.objects.create(**history_data)
                except Exception:
                    db_wallet = None

            try:
                referral_and_earn = ReferralAndEarn.objects.get(
                    customer=instance.customer,
                    transaction__status=TransactionStatus.WATING,
                )
                transaction = referral_and_earn.transaction
            except Exception:
                transaction = None

            if transaction:
                amount = 0.0
                try:
                    _transaction = Transaction.objects.get(pk=transaction.pk)
                    amount = _transaction.amount
                    customer_wallet = _transaction.customer_wallet
                except Exception:
                    _transaction = None
                    customer_wallet = None

                if _transaction and customer_wallet and amount:
                    try:
                        _customer_wallet = CustomerWallet.objects.get(
                            pk=customer_wallet.pk
                        )

                        ####### added into money #######
                        _customer_wallet.balance_amount = (
                            _customer_wallet.balance_amount + amount
                        )
                        _customer_wallet.is_active = True
                        _customer_wallet.save()
                        ####### added into money #######

                        ####### transaction is successful #######
                        _transaction.status = TransactionStatus.SUCCESSFUL
                        _transaction.save()
                        ####### transaction is successful #######
                    except Exception:
                        pass

        ##### order cancel #####
        if instance.order_status == OrderStatus.ORDER_CANCEL:
            if instance.transaction:
                try:
                    _transaction = Transaction.objects.get(pk=transaction.pk)
                except Exception:
                    _transaction = None

                if _transaction:
                    try:
                        ####### transaction is failed #######
                        _transaction.status = TransactionStatus.FAILED
                        _transaction.save()
                        ####### transaction is failed #######
                    except Exception:
                        pass
    return True
