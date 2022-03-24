import json

from dateutil import relativedelta
from django.db.models import Q
from django.utils import timezone
from service.payment.client import PaymentClient
from v1.membership.choice import MembershipTypeChoices
from v1.wallet.choice import (
    TransactionMethod,
    TransactionPlatform,
    TransactionStatus,
    TransactionType,
)
from v1.wallet.models import Transaction

from .models import Membership, MembershipPlain


def customer_has_exist_membership(customer=None):
    if not customer:
        return False

    now = timezone.now()
    query_filter = Q()

    query_filter.add(Q(customer=customer), Q.AND)
    query_filter.add(Q(start_at__lte=now, end_at__gte=now), Q.AND)

    return (
        Membership.objects.filter(
            query_filter,
        )
        .exclude(is_active=False)
        .exists()
    )


def get_membership_plan(type):
    return MembershipPlain.objects.get_or_create(type=type)


def get_one_month_plan():
    plan_one_month = MembershipTypeChoices.ONE_MONTH
    plan, create_plan = get_membership_plan(plan_one_month)

    #  if plan are not exist then set default amount
    if create_plan:
        plan.mrp_amount = 99.00
        plan.discount_amount = 99.00
        plan.save()
    return plan


def set_membership(customer, type, is_payment_done=False, is_payment_in_cash=False):
    membership, created = Membership.objects.get_or_create(customer=customer)

    # One month
    if type == MembershipTypeChoices.ONE_MONTH:
        plan, create_plan = get_membership_plan(type)

        #  if plan are not exist then set default amount
        if create_plan:
            plan.mrp_amount = 99.00
            plan.discount_amount = 99.00
            plan.save()

        if membership.is_active:
            membership.end_at = membership.end_at + relativedelta.relativedelta(
                months=1
            )
        else:
            membership.start_at = timezone.now()
            membership.end_at = timezone.now() + relativedelta.relativedelta(months=1)

        membership.plan = plan
        membership.amount = plan.discount_amount

    # Three month
    elif type == MembershipTypeChoices.THREE_MONTH:
        plan, create_plan = get_membership_plan(type)

        #  if plan are not exist then set default amount
        if create_plan:
            plan.mrp_amount = 249.00
            plan.discount_amount = 249.00
            plan.save()

        if membership.is_active:
            membership.end_at = membership.end_at + relativedelta.relativedelta(
                months=3
            )
        else:
            membership.start_at = timezone.now()
            membership.end_at = timezone.now() + relativedelta.relativedelta(months=3)

        membership.plan = plan
        membership.amount = plan.discount_amount

    # Half year
    elif type == MembershipTypeChoices.HALF_YEAR:
        plan, create_plan = get_membership_plan(type)

        #  if plan are not exist then set default amount
        if create_plan:
            plan.mrp_amount = 399.00
            plan.discount_amount = 399.00
            plan.save()

        if membership.is_active:
            membership.end_at = membership.end_at + relativedelta.relativedelta(
                months=6
            )
        else:
            membership.start_at = timezone.now()
            membership.end_at = timezone.now() + relativedelta.relativedelta(months=6)

        membership.plan = plan
        membership.amount = plan.discount_amount

    # One year
    elif type == MembershipTypeChoices.ONE_YEAR:
        plan, create_plan = get_membership_plan(type)

        #  if plan are not exist then set default amount
        if create_plan:
            plan.mrp_amount = 599.00
            plan.discount_amount = 599.00
            plan.save()

        if membership.is_active:
            membership.end_at = membership.end_at + relativedelta.relativedelta(year=1)
        else:
            membership.start_at = timezone.now()
            membership.end_at = timezone.now() + relativedelta.relativedelta(year=1)

        membership.plan = plan
        membership.amount = plan.discount_amount

    # if payment is successfully to automatically set is active
    if is_payment_done:
        membership.is_active = True

    transaction_data = {
        "name": "Adding membership by {}".format(membership.customer.get_full_name()),
        "notes": "Adding membership by {}".format(membership.customer.get_full_name()),
        "transaction_type": TransactionType.ADD_MEMBERSHIP,
        "method": TransactionMethod.DEBIT,
        "status": TransactionStatus.SUCCESSFUL
        if is_payment_done
        else TransactionStatus.WATING,
        "platform": TransactionPlatform.CASH
        if is_payment_in_cash
        else TransactionPlatform.ONLINE,
        "datetime": timezone.now(),
        "amount": membership.amount,
    }
    membership_transaction = Transaction.objects.create(**transaction_data)
    membership.transaction = membership_transaction
    membership.save()

    #  if none or payment is pending to create membership
    if not is_payment_done or is_payment_done == False:
        ##### Create payment
        membership.refresh_from_db()
        paymet_data = {
            "orderId": str(membership_transaction.reference),
            "orderAmount": membership.amount,
            "orderCurrency": "INR",
        }
        payment_client = PaymentClient()
        print("===========")
        print(paymet_data)
        print("===========")
        response = payment_client.create_order(paymet_data)
        ##### Create payment

        ##### Membership payment payload save
        membership_transaction.payment_payload = json.dumps(response)
        membership_transaction.save()
        ##### Membership payment payload save

        membership.payment_token = response.get("cftoken")

    membership.save()
    # TODO: sending mail
    # TODO: sending sms
    return membership
