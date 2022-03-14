from config.celery import app
from v1.promotion.models import DiscountVoucher
from django.utils import timezone
from django.db.models import Q


@app.task
def change_the_discount_order():
    discounts = DiscountVoucher.objects.filter(is_active=True).exclude(is_deleted=True)
    for i, item in enumerate(discounts):
        item.priority = i + 1
        item.save()
    return True


@app.task
def automatic_change_activity_after_expired_voucher():
    query_filter = Q()
    query_filter.add(
        Q(
            end_date__isnull=False,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
        ),
        Q.AND,
    )
    query_filter.add(Q(is_active=True), Q.AND)

    discounts = DiscountVoucher.objects.filter(query_filter).exclude(
        is_deleted=True, is_active=False
    )
    for discount in discounts:
        discount.is_active = False
        discount.save()
    print("----------------------set_automatically_deactivate_voucher_after_expired")
    return True
