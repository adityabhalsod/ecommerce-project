from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import User
from base.serializers import BaseSerializer
from v1.catalog.models import Category, Product, Variation
from v1.promotion.models import DiscountVoucher, ReferralAndEarn
from v1.promotion.tasks import change_the_discount_order
from v1.store.models import Store
from constance import config
from account.serializers import ProfileSerializer

from v1.wallet.tasks import referral_and_earn_wallet


class DiscountVoucherSerializer(BaseSerializer):
    store_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        many=True,
        write_only=True,
    )
    product_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Product.objects.exclude(is_deleted=True),
        source="products",
        many=True,
        write_only=True,
    )
    variation_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Variation.objects.exclude(is_deleted=True),
        source="variants",
        many=True,
        write_only=True,
    )
    category_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Category.objects.exclude(is_deleted=True),
        source="categories",
        many=True,
        write_only=True,
    )

    class Meta:
        model = DiscountVoucher
        fields = "__all__"
        read_only_fields = ("terms_and_conditions",)

    def create(self, validated_data):
        instance = super(DiscountVoucherSerializer, self).create(validated_data)
        change_the_discount_order.delay()
        return instance

    def update(self, instance, validated_data):
        instance = super(DiscountVoucherSerializer, self).update(
            instance, validated_data
        )
        change_the_discount_order.delay()
        return instance


class DiscountVoucherReadOnlySerializer(BaseSerializer):
    class Meta:
        model = DiscountVoucher
        fields = (
            "type",
            "code",
            "name",
            "description",
            "is_code_required",
            "min_amount",
            "is_exist_min_amount",
            "discount_value",
            "value_type",
            "is_apply_super_saving_days_item",
            "is_apply_exclusive_offer_item",
            "is_apply_free_delivery",
            "min_checkout_items_quantity",
            "usage_limit",
            "used",
            "priority",
            "start_date",
            "end_date",
            "is_active",
        )
        read_only_fields = (
            "type",
            "code",
            "name",
            "description",
            "is_code_required",
            "min_amount",
            "is_exist_min_amount",
            "discount_value",
            "value_type",
            "is_apply_super_saving_days_item",
            "is_apply_exclusive_offer_item",
            "is_apply_free_delivery",
            "min_checkout_items_quantity",
            "usage_limit",
            "used",
            "priority",
            "start_date",
            "end_date",
            "is_active",
            "terms_and_conditions",
        )


class ReferralAndEarnSerializer(BaseSerializer):
    generated_referral_code = serializers.SlugRelatedField(
        slug_field="referral_code",
        queryset=User.objects.exclude(is_deleted=True),
        source="refer_customer",
        write_only=True,
    )
    refer_customer = ProfileSerializer(read_only=True)
    customer = ProfileSerializer(read_only=True)

    class Meta:
        model = ReferralAndEarn
        fields = (
            "generated_referral_code",
            "refer_customer",
            "customer",
            "referral_code",
            "earn_amount",
            "transaction",
        )
        read_only_fields = (
            "refer_customer",
            "customer",
            "referral_code",
            "earn_amount",
            "transaction",
        )

    def validate(self, attrs):
        request = self.context.get("request")
        if not request.user:
            raise ValidationError(
                {"customer": "Customer are not found on current request."}
            )

        if not request.user.is_authenticated:
            raise ValidationError({"customer": "Customer are not authenticate."})

        if not request.user.is_profile_completely_filled:
            raise ValidationError(
                {"customer": "This customer are not fullfil the own profile."}
            )

        if User.objects.filter(
            pk=request.user.pk, referral_code=attrs.get("referral_code")
        ).exists():
            raise ValidationError(
                {"generated_referral_code": "This referral code is not use at self."}
            )

        if not attrs.get("refer_customer"):
            raise ValidationError(
                {
                    "generated_referral_code": "This generate referral code according customer are not exist."
                }
            )

        refer_customer = attrs.get("refer_customer")
        attrs["referral_code"] = refer_customer.referral_code
        attrs["customer"] = request.user
        attrs["earn_amount"] = config.REFER_AND_EARN_PRICE
        return attrs

    def create(self, validated_data):
        instance = super(ReferralAndEarnSerializer, self).create(validated_data)
        transaction = referral_and_earn_wallet(
            instance.refer_customer, instance.earn_amount
        )
        # Added transaction reference number
        instance.transaction = transaction
        instance.save()
        return instance
