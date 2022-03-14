from constance import config
from rest_framework.exceptions import ValidationError
from v1.delivery.models import DeliveryCharges
from v1.membership.calculation import customer_has_exist_membership, get_one_month_plan
from v1.orders.choice import OrderStatus
from v1.orders.models import Order
from v1.promotion.calculation import (
    calculate_discount_for_final_amount,
    check_has_delivery_is_free,
)

from .models import Cart


def get_delivery_charge(amount):
    final_delivery_charge = 0.0
    delivery_charges = DeliveryCharges.objects.exclude(is_active=False, is_deleted=True)
    for charge in delivery_charges:
        if amount in range(
            int(charge.amount_starting_range), int(charge.amount_ending_range)
        ):
            final_delivery_charge = charge.delivery_charge
    return final_delivery_charge


def item_price_set(item, has_exist_membership, new_membership_adding):
    # Item price calculation
    item_rate = item.product_variation.our_rate
    tax = 0.0

    # exclusive_rate
    if (
        item.product_variation.product_stock_master
        and item.product_variation.product_stock_master.is_exclusive_item
        and item.product_variation.exclusive_rate
        and item.product_variation.exclusive_rate < item_rate
    ):
        item_rate = item.product_variation.exclusive_rate

    # membership rate
    if has_exist_membership or new_membership_adding:
        if item.product_variation.member_rate < item_rate:
            item_rate = item.product_variation.member_rate

    # final product item tax
    if (
        item_rate > 0
        and item.product_variation.product_stock_master
        and item.product_variation.product_stock_master.product
        and item.product_variation.product_stock_master.product.tax
    ):
        tax = (
            float(item_rate)
            * float(item.product_variation.product_stock_master.product.tax)
        ) / 100
        item_rate = float(item_rate) + float(tax)

    return item_rate, tax


def cart_calculation(customer, new_membership_adding=False, voucher_pk=None):
    data = {}
    carts = Cart.objects.filter(customer=customer).exclude(is_deleted=True)
    if not carts.exists():
        raise ValidationError({"cart": "Cart is empty!."})

    if voucher_pk:
        voucher_pk = int(voucher_pk)

    our_store_saving = 0.0
    membership_saving = 0.0
    final_amount = 0.0
    final_quantity = 0
    final_delivery_charge = 0.0
    final_discount = 0.0
    final_total = 0.0
    final_membership_fee = 0.0
    final_tax = 0.0

    has_exist_membership = customer_has_exist_membership(customer)

    if carts:
        for item in carts:
            final_quantity = final_quantity + item.quantity
            if item.product_variation:
                # our_store_saving
                our_store_saving = (
                    our_store_saving + item.product_variation.our_rate_difference
                )

                # membership_saving
                membership_saving = (
                    membership_saving + item.product_variation.member_rate_difference
                )

                # final amount
                item_rate, tax = item_price_set(
                    item, has_exist_membership, new_membership_adding
                )
                final_tax = final_tax + tax
                final_amount = final_amount + (item_rate * item.quantity)

        final_total = final_amount

        if final_amount != 0.0:
            if (
                Order.objects.filter(customer=customer)
                .exclude(
                    is_deleted=True,
                    order_status__in=[
                        OrderStatus.NOT_ATTEMPT,
                        OrderStatus.ORDER_CANCEL,
                    ],
                )
                .exists()
            ):
                if (
                    check_has_delivery_is_free(
                        final_amount, final_quantity, voucher_pk=voucher_pk
                    )
                    == False
                ):
                    final_delivery_charge = get_delivery_charge(amount=final_amount)
            else:
                if config.FIRST_ORDER_DELIVERY_CHARGE:
                    if (
                        check_has_delivery_is_free(
                            final_amount, final_quantity, voucher_pk=voucher_pk
                        )
                        == False
                    ):
                        final_delivery_charge = get_delivery_charge(amount=final_amount)

        # calculation of discount
        if final_amount != 0.0:
            final_discount = calculate_discount_for_final_amount(
                final_amount, final_quantity, voucher_pk=voucher_pk
            )

        # Added delivery charge
        final_total = final_total + final_delivery_charge

        # Added discount
        final_total = final_total - final_discount

        # Added membership fee in this order
        if new_membership_adding:
            plan = get_one_month_plan()
            final_membership_fee = plan.discount_amount
            final_total = final_total + final_membership_fee

    # final
    # TODO: Wallet money [pending]
    data["final_tax"] = final_tax
    data["final_amount"] = final_amount
    data["final_quantity"] = final_quantity
    data["final_total"] = final_total
    data["final_delivery_charge"] = final_delivery_charge
    data["final_discount"] = final_discount
    data["final_membership_fee"] = final_membership_fee
    data["our_store_saving"] = our_store_saving
    data["membership_saving"] = membership_saving
    return data
