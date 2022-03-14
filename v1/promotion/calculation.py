from django.utils import timezone

from django.db.models import Q
from v1.promotion.choice import ValueType, VoucherType

from .models import DiscountVoucher


def calculate_discount_for_final_amount(
    final_amount, min_checkout_items_quantity, voucher_pk=None
):
    def validation_level_two(discount, final_amount):
        if discount.value_type == ValueType.FIXED:
            return discount.discount_value
        elif discount.value_type == ValueType.PERCENTAGE:
            return float(float(final_amount) * float(discount.discount_value)) / 100
        return 0.0

    def validation_level_one(discount, final_amount):
        if discount.is_exist_min_amount:
            if final_amount >= discount.min_amount:
                return validation_level_two(discount, final_amount)
            return validation_level_two(discount, final_amount)
        return 0.0

    filter_query = Q(is_active=True, type=VoucherType.ENTIRE_ORDER)
    filter_query.add(
        Q(Q(type=VoucherType.ENTIRE_ORDER) & Q(is_code_required=False)),
        Q.AND,
    )
    if voucher_pk and isinstance(voucher_pk, int):
        filter_query.add(
            Q(Q(pk=voucher_pk) & Q(is_code_required=True)),
            Q.OR,
        )

    all_discount = DiscountVoucher.objects.filter(filter_query).order_by("priority")
    now = timezone.now()
    for discount in all_discount:
        if discount.discount_value:
            if discount.end_date:
                if now >= discount.end_date:
                    return 0.0
                else:
                    if (
                        discount.min_checkout_items_quantity
                        and discount.min_checkout_items_quantity != 0
                    ):
                        if (
                            discount.min_checkout_items_quantity
                            <= min_checkout_items_quantity
                        ):
                            return validation_level_one(discount, final_amount)
                    else:
                        return validation_level_one(discount, final_amount)

            if (
                discount.min_checkout_items_quantity
                and discount.min_checkout_items_quantity != 0
            ):
                if discount.min_checkout_items_quantity <= min_checkout_items_quantity:
                    return validation_level_one(discount, final_amount)
            else:
                return validation_level_one(discount, final_amount)

    return 0.0


def check_has_delivery_is_free(
    final_amount, min_checkout_items_quantity, voucher_pk=None
):
    def validation_level_one(discount, final_amount):
        if discount.is_exist_min_amount:
            if final_amount >= discount.min_amount:
                return True
            return True
        return False

    filter_query = Q()
    filter_query.add(
        Q(
            type=VoucherType.ENTIRE_ORDER,
            is_code_required=False,
            is_apply_free_delivery=True,
            is_active=True,
        ),
        Q.AND,
    )
    if voucher_pk and isinstance(voucher_pk, int):
        filter_query.add(
            Q(
                pk=voucher_pk,
                type=VoucherType.ENTIRE_ORDER,
                is_code_required=True,
                is_apply_free_delivery=True,
                is_active=True,
            ),
            Q.AND,
        )

    all_discount = DiscountVoucher.objects.filter(filter_query).order_by("priority")
    now = timezone.now()
    for discount in all_discount:
        if discount.end_date:
            if now >= discount.end_date:
                return False
            else:
                if (
                    discount.min_checkout_items_quantity
                    and discount.min_checkout_items_quantity != 0
                ):
                    if (
                        discount.min_checkout_items_quantity
                        <= min_checkout_items_quantity
                    ):
                        return True
                else:
                    return True

        if (
            discount.min_checkout_items_quantity
            and discount.min_checkout_items_quantity != 0
        ):
            if discount.min_checkout_items_quantity <= min_checkout_items_quantity:
                return validation_level_one(discount, final_amount)
        else:
            return validation_level_one(discount, final_amount)
    return False
