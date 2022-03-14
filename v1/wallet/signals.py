from dateutil import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from v1.membership.choice import MembershipTypeChoices
from v1.membership.models import Membership
from v1.wallet.choice import TransactionPlatform, TransactionStatus, TransactionType
from v1.wallet.models import CustomerWallet, DeliveryBoyWallet, Transaction


@receiver(post_save, sender=CustomerWallet)
def customer_wallet_effect(sender, instance, created, **kwargs):
    return True


@receiver(post_save, sender=DeliveryBoyWallet)
def delivery_boy_wallet_effect(sender, instance, created, **kwargs):
    return True


@receiver(post_save, sender=Transaction)
def transaction_update(sender, instance, created, **kwargs):
    if instance:
        if instance.transaction_type == TransactionType.ADD_MONEY_IN_WALLET:
            if instance.status == TransactionStatus.SUCCESSFUL:
                try:
                    customer_wallet = CustomerWallet.objects.get(
                        customer=instance.customer_wallet.pk
                    )
                    # Added money in wallet
                    final_amount = float(customer_wallet.balance_amount) + float(
                        instance.amount
                    )
                    customer_wallet.balance_amount = final_amount
                    customer_wallet.is_active = True
                    customer_wallet.save()
                except Exception as e:
                    print("Customer wallet are not found!.")
        elif instance.transaction_type == TransactionType.ADD_MEMBERSHIP:
            if (
                instance.status == TransactionStatus.SUCCESSFUL
                and instance.platform == TransactionPlatform.ONLINE
            ):
                now = timezone.now()
                try:
                    membership = Membership.objects.get(transaction__pk=instance.pk)
                    membership.start_at = now

                    if membership.plan:
                        if membership.plan.type == MembershipTypeChoices.ONE_MONTH:
                            membership.end_at = now + relativedelta.relativedelta(
                                months=1
                            )

                        elif membership.plan.type == MembershipTypeChoices.THREE_MONTH:
                            membership.end_at = now + relativedelta.relativedelta(
                                months=3
                            )

                        elif membership.plan.type == MembershipTypeChoices.HALF_YEAR:
                            membership.end_at = now + relativedelta.relativedelta(
                                months=6
                            )

                        elif membership.plan.type == MembershipTypeChoices.ONE_YEAR:
                            membership.end_at = now + relativedelta.relativedelta(
                                year=1
                            )

                    membership.is_active = True
                    membership.save()
                except Exception as e:
                    print("Customer wallet are not found!.")

    return True
