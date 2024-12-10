from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from account.models import User
from account.serializers import ProfileSerializer
from base.serializers import BaseSerializer
from v1.store.models import Store
from v1.store.serializers import StoreExcloudGeoLocationSerializer

from .models import (
    PackageBoy,
)


class PackageBoyCRUDSerializer(BaseSerializer):
    user = ProfileSerializer(read_only=True)
    user_id = serializers.SlugRelatedField(
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        source="user",
        write_only=True,
        required=False,
    )
    store = StoreExcloudGeoLocationSerializer(read_only=True)
    store_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Store.objects.exclude(is_deleted=True),
        source="store",
        write_only=True,
    )

    class Meta:
        model = PackageBoy
        fields = "__all__"
