from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import User
from account.serializers import ProfileSerializer
from base.serializers import BaseSerializer
from v1.store.models import Store
from v1.warehouse.models import Warehouse


class StoreCRUDSerializer(BaseSerializer):
    manager = ProfileSerializer(read_only=True)
    manager_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        source="manager",
        write_only=True,
    )
    warehouse_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Warehouse.objects.exclude(is_deleted=True),
        source="warehouse",
        write_only=True,
    )

    class Meta:
        model = Store
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get("is_address_set_manually", False) == False and not attrs.get(
            "geo_location", None
        ):
            raise ValidationError(
                {
                    "geo_location": "While geo location are empty then set `is_address_set_manually:true` rather then, please adding geo location."
                }
            )

        return attrs


class StoreExcloudGeoLocationSerializer(BaseSerializer):
    manager = ProfileSerializer(read_only=True)
    manager_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        source="manager",
        write_only=True,
    )

    class Meta:
        model = Store
        exclude = (
            "geo_location",
            "allow_geo_location_path",
        )
