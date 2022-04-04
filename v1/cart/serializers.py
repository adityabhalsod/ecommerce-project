from constance import config
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.choice import SystemDefaultGroup
from account.serializers import ProfileSerializer
from base.serializers import BaseSerializer
from v1.cart.calculation import get_delivery_charge, item_price_set
from v1.cart.choice import OrderType
from v1.catalog.models import Variation
from v1.catalog.serializers import VariationCRUDSerializer
from v1.membership.calculation import customer_has_exist_membership, get_one_month_plan
from v1.orders.choice import OrderStatus, order_expired
from v1.orders.models import FinalDeliveredOrder, Order
from v1.orders.tasks import order_payment_creating, order_cash_on_delivery_creating
from v1.promotion.calculation import (
    calculate_discount_for_final_amount,
    check_has_delivery_is_free,
)
from v1.promotion.models import DiscountVoucher
from v1.store.models import Store
from v1.store.serializers import StoreExcloudGeoLocationSerializer
from .models import Cart, Checkout


class CartCRUDSerializer(BaseSerializer):
    product_variation = VariationCRUDSerializer(read_only=True)
    product_variation_id = serializers.SlugRelatedField(
        required=True,
        slug_field="id",
        queryset=Variation.objects.exclude(is_deleted=True),
        source="product_variation",
        write_only=True,
    )
    customer = ProfileSerializer(read_only=True)
    store = StoreExcloudGeoLocationSerializer(read_only=True)
    store_id = serializers.SlugRelatedField(
        required=True,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        write_only=True,
    )

    class Meta:
        model = Cart
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get("request")
        if not request.user:
            raise ValidationError(
                {"customer": "Customer are not found on current request."}
            )

        if not request.user.groups.filter(name=SystemDefaultGroup.CUSTOMER).exists():
            raise ValidationError({"customer": "User is not customer."})

        attrs["customer"] = request.user
        product_variation = attrs.get("product_variation")
        quantity = attrs.get("quantity", 1)
        if product_variation and (quantity > product_variation.max_order_quantity):
            raise ValidationError(
                {
                    "max_order_quantity": "Sorry, You can not add more quantity of this product in cart"
                }
            )
        return attrs


class CheckoutCRUDSerializer(BaseSerializer):
    customer = ProfileSerializer(read_only=True)
    store = StoreExcloudGeoLocationSerializer(read_only=True)
    store_id = serializers.SlugRelatedField(
        required=True,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        write_only=True,
    )
    discount_and_voucher_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DiscountVoucher.objects.exclude(is_active=False, is_deleted=True),
        source="discount_and_voucher",
        write_only=True,
    )
    order_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Checkout
        fields = "__all__"

    def get_order_id(self, obj):
        if obj and obj.order:
            return obj.order.pk
        return None

    def validate(self, attrs):
        request = self.context.get("request")
        if not request.user:
            raise ValidationError(
                {"customer": "Customer are not found on current request."}
            )

        if not request.user.groups.filter(name=SystemDefaultGroup.CUSTOMER).exists():
            raise ValidationError({"customer": "User is not customer."})

        customer = request.user
        attrs["customer"] = customer

        if not Cart.objects.filter(customer=customer).exclude(is_deleted=True).exists():
            raise ValidationError({"cart": "Cart is empty!."})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        host_protocol = "https" if request.is_secure() else "http"
        http_host = request.META.get("HTTP_HOST")
        checkout_data = {}

        if not validated_data.get("customer"):
            raise ValidationError(
                {"customer": "Customer are not found on current request."}
            )

        customer = validated_data.get("customer")
        new_membership_adding = validated_data.get("new_membership_adding", False)

        discount_and_voucher_id = None
        if validated_data.get("discount_and_voucher", None):
            discount_and_voucher = validated_data.get("discount_and_voucher")
            discount_and_voucher_id = discount_and_voucher.pk

        carts = Cart.objects.filter(customer=customer).exclude(is_deleted=True)

        if not carts.exists():
            raise ValidationError({"cart": "Cart is empty!."})

        our_store_saving = 0.0
        membership_saving = 0.0
        final_tax = 0.0
        final_amount = 0.0
        final_quantity = 0
        final_delivery_charge = 0.0
        final_discount = 0.0
        final_total = 0.0
        final_membership_fee = 0.0

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
                        membership_saving
                        + item.product_variation.member_rate_difference
                    )

                    # final amount
                    item_rate, tax = item_price_set(
                        item, has_exist_membership, new_membership_adding
                    )
                    final_tax = final_tax + tax
                    final_amount = final_amount + (item_rate * float(item.quantity))

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
                            final_amount,
                            final_quantity,
                            voucher_pk=discount_and_voucher_id,
                        )
                        == False
                    ):
                        final_delivery_charge = get_delivery_charge(amount=final_amount)
                else:
                    if config.FIRST_ORDER_DELIVERY_CHARGE:
                        if (
                            check_has_delivery_is_free(
                                final_amount,
                                final_quantity,
                                voucher_pk=discount_and_voucher_id,
                            )
                            == False
                        ):
                            final_delivery_charge = get_delivery_charge(
                                amount=final_amount
                            )

            # calculation of discount
            if final_amount != 0.0:
                final_discount = calculate_discount_for_final_amount(
                    final_amount,
                    final_quantity,
                    voucher_pk=discount_and_voucher_id,
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

            #  set final delivery boy tip
            if validated_data.get("final_delivery_boy_tip", 0.0):
                final_total = final_total + validated_data.get(
                    "final_delivery_boy_tip", 0.0
                )

        # final
        # TODO: Wallet money [pending]
        checkout_data["final_tax"] = final_tax
        checkout_data["final_amount"] = final_amount
        checkout_data["final_quantity"] = final_quantity
        checkout_data["final_total"] = final_total
        checkout_data["final_delivery_charge"] = final_delivery_charge
        checkout_data["final_discount"] = final_discount
        checkout_data["final_membership_fee"] = final_membership_fee
        checkout_data["our_store_saving"] = our_store_saving
        checkout_data["membership_saving"] = membership_saving

        if checkout_data.get("final_amount", 0.0) == 0.0:
            raise ValidationError({"final_amount": "0 Rs. not create order."})

        final_data = {**validated_data, **checkout_data}

        # While order type has been set to also set as order type.
        if (
            validated_data.get("order_type", OrderType.ONLINE)
            == OrderType.CASH_ON_DELIVERY
            and config.MAXIMUM_CASE_DELIVERY < final_total
        ):
            raise ValidationError(
                {
                    "order_type": "We are allowing only maximum {} Rs. on cash on delivery.".format(
                        config.MAXIMUM_CASE_DELIVERY
                    )
                }
            )

        checkout = super(CheckoutCRUDSerializer, self).create(final_data)

        order_data = {
            "customer": checkout.customer,
            "store": checkout.store,
            "order_date": timezone.now(),
            "total_amount": checkout.final_total,
            "total_quantity": checkout.final_quantity,
            "no_contact_delivery": checkout.no_contact_delivery,
            "final_delivery_boy_tip": checkout.final_delivery_boy_tip,
            "new_membership_adding": checkout.new_membership_adding,
            "our_store_saving": checkout.our_store_saving,
            "membership_saving": checkout.membership_saving,
            "membership_type": checkout.membership_type,
            "final_membership_fee": checkout.final_membership_fee,
            "order_type": checkout.order_type,
        }

        if checkout.order_type == OrderType.CASH_ON_DELIVERY:
            order_data["order_status"] = OrderStatus.ORDER_PLACED
            order = Order.objects.create(**order_data)
            order_cash_on_delivery_creating.delay(order)
            checkout.order = order
            checkout.save()
        else:
            order_data["order_status"] = OrderStatus.ORDER_AWAITING_FOR_PAYMENT
            order = Order.objects.create(**order_data)
            checkout.order = order
            checkout.save()
            paymet_data = {
                "orderId": str(order.order_number),
                "orderAmount": checkout.final_total,
                "orderCurrency": "INR",
            }
            order_payment_creating.delay(paymet_data, order)

        if not order:
            raise ValidationError(
                {"order": "order are not created please try again later."}
            )

        if carts:
            for item in carts:
                if item.product_variation:
                    # final amount
                    item_rate, tax = item_price_set(
                        item, has_exist_membership, new_membership_adding
                    )
                    final_order_data = {
                        "customer": checkout.customer,
                        "store": checkout.store,
                        "product_variation": item.product_variation,
                        "order": order,
                        "checkout": checkout,
                        "rate": item_rate,
                        "quantity": item.quantity,
                        "amount": item_rate * float(item.quantity),
                    }
                    FinalDeliveredOrder.objects.create(**final_order_data)
        return checkout
