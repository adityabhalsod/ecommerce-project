from account.serializers import ProfileSerializer
from base.serializers import BaseSerializer
from rest_framework import serializers
from v1.catalog.serializers import VariationReadOnlySerializer
from v1.delivery.models import DeliveryBoy
from v1.delivery.serializers import DeliveryBoyCRUDSerializer
from v1.package.models import PackageBoy
from v1.package.serializers import PackageBoyCRUDSerializer
from v1.promotion.serializers import DiscountVoucherReadOnlySerializer
from v1.store.serializers import StoreExcloudGeoLocationSerializer

from .models import FinalDeliveredOrder, Order


class FinalDeliverdOrderCRUDSerializer(BaseSerializer):
    discount_and_voucher = DiscountVoucherReadOnlySerializer(read_only=True)
    product_variation = VariationReadOnlySerializer(read_only=True)

    class Meta:
        model = FinalDeliveredOrder
        fields = (
            "product_variation",
            "rate",
            "quantity",
            "amount",
            "discount_and_voucher",
        )


class OrderCRUDSerializer(BaseSerializer):
    customer = ProfileSerializer(read_only=True)
    delivery_boy = DeliveryBoyCRUDSerializer(read_only=True)
    package_boy = PackageBoyCRUDSerializer(read_only=True)
    store = StoreExcloudGeoLocationSerializer(read_only=True)
    items = serializers.SerializerMethodField(
        read_only=True,
        required=False,
    )
    discount_and_voucher = DiscountVoucherReadOnlySerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("order_number",)

    def get_items(self, obj):
        data = obj.final_delivered_order.all()
        if not data:
            return []
        return FinalDeliverdOrderCRUDSerializer(
            data, many=True, context={"request": self.context.get("request")}
        ).data


class OrderMutationSerializer(BaseSerializer):
    delivery_boy = DeliveryBoyCRUDSerializer(
        read_only=True,
        required=False,
    )
    delivery_boy_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoy.objects.exclude(is_deleted=True),
        source="delivery_boy",
    )
    package_boy = PackageBoyCRUDSerializer(
        read_only=True,
        required=False,
    )
    package_boy_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=PackageBoy.objects.exclude(is_deleted=True),
        source="package_boy",
    )

    class Meta:
        model = Order
        fields = (
            "delivery_boy_id",
            "delivery_boy",
            "package_boy_id",
            "package_boy",
            "order_status",
            "package_size",
            "package_weight",
            "delivery_time_start",
            "delivery_time_end",
            "package_time_start",
            "package_time_end",
            "dropzone",
        )
