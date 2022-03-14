from django.utils.translation import ugettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from account.models import User
from account.serializers import ProfileSerializer
from base.serializers import BaseSerializer
from v1.store.models import Store
from v1.store.serializers import StoreExcloudGeoLocationSerializer

from .models import (
    DeliveryBoy,
    DeliveryBoyDocument,
    DeliveryBoyPayoutInformation,
    DeliveryBoyReview,
    DeliveryBoyVehicleInformation,
    DeliveryBoyVehiclePhotos,
    DeliveryCharges,
)


class DeliveryBoyCRUDSerializer(BaseSerializer):
    user = ProfileSerializer(read_only=True)
    user_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        source="user",
        write_only=True,
    )
    store = StoreExcloudGeoLocationSerializer(read_only=True, many=True)
    store_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        write_only=True,
    )

    class Meta:
        model = DeliveryBoy
        fields = "__all__"
        read_only_fields = (
            "user",
            "is_approve",
            "status",
            "payout_balance",
        )


class DeliveryBoyPayoutCRUDSerializer(BaseSerializer):
    delivery_boy = DeliveryBoyCRUDSerializer(read_only=True)
    delivery_boy_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoy.objects.exclude(is_deleted=True),
        source="delivery_boy",
        write_only=True,
    )
    bank_account_proof = Base64ImageField(required=False)

    class Meta:
        model = DeliveryBoyPayoutInformation
        fields = "__all__"


class DeliveryBoyDocumentCRUDSerializer(BaseSerializer):
    back = Base64ImageField(required=False)
    front = Base64ImageField(required=False)

    delivery_boy = DeliveryBoyCRUDSerializer(read_only=True)
    delivery_boy_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoy.objects.exclude(is_deleted=True),
        source="delivery_boy",
        write_only=True,
    )

    class Meta:
        model = DeliveryBoyDocument
        fields = "__all__"
        read_only_fields = ("status",)


class DeliveryBoyDocumentCRUDAdminAccessSerializer(BaseSerializer):
    back = Base64ImageField(required=False)
    front = Base64ImageField(required=False)

    delivery_boy = DeliveryBoyCRUDSerializer(read_only=True)
    delivery_boy_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoy.objects.exclude(is_deleted=True),
        source="delivery_boy",
        write_only=True,
    )

    class Meta:
        model = DeliveryBoyDocument
        fields = "__all__"


class DeliveryBoyReviewCRUDSerializer(BaseSerializer):
    delivery_boy = DeliveryBoyCRUDSerializer(read_only=True)
    delivery_boy_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoy.objects.exclude(is_deleted=True),
        source="delivery_boy",
        write_only=True,
    )
    author = ProfileSerializer(read_only=True)
    author_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        source="author",
        write_only=True,
    )

    class Meta:
        model = DeliveryBoyReview
        fields = "__all__"


class DeliveryBoyVehiclePhotosCRUDSerializer(BaseSerializer):
    original = Base64ImageField(required=False)

    class Meta:
        model = DeliveryBoyVehiclePhotos
        fields = "__all__"


class DeliveryBoyVehicleInformationCRUDSerializer(BaseSerializer):
    photos = DeliveryBoyVehiclePhotosCRUDSerializer(read_only=True, many=True)
    photo_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoyVehiclePhotos.objects.exclude(is_deleted=True),
        source="photos",
        write_only=True,
        many=True,
    )
    delivery_boy = DeliveryBoyCRUDSerializer(read_only=True)
    delivery_boy_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoy.objects.exclude(is_deleted=True),
        source="delivery_boy",
        write_only=True,
    )

    class Meta:
        model = DeliveryBoyVehicleInformation
        fields = "__all__"
        read_only_fields = ("status",)


class DeliveryBoyVehicleInformationCRUDAdminAccessSerializer(BaseSerializer):
    photos = DeliveryBoyVehiclePhotosCRUDSerializer(read_only=True, many=True)
    photo_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoyVehiclePhotos.objects.exclude(is_deleted=True),
        source="photos",
        write_only=True,
        many=True,
    )
    delivery_boy = DeliveryBoyCRUDSerializer(read_only=True)
    delivery_boy_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=DeliveryBoy.objects.exclude(is_deleted=True),
        source="delivery_boy",
        write_only=True,
    )

    class Meta:
        model = DeliveryBoyVehicleInformation
        fields = "__all__"


class DeliveryChargesCRUDSerializer(BaseSerializer):
    class Meta:
        model = DeliveryCharges
        fields = "__all__"
