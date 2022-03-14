from rest_framework import serializers
from account.models import User
from account.serializers import ProfileSerializer
from base.serializers import BaseSerializer

from .models import Reason, ReasonType


class ReasonTypeCRUDSerializer(BaseSerializer):
    class Meta:
        model = ReasonType
        fields = "__all__"


class ReasonCRUDSerializer(BaseSerializer):
    create_by = ProfileSerializer(read_only=True)
    create_by_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        source="create_by",
        write_only=True,
    )

    reason_for = ReasonTypeCRUDSerializer(required=False)
    reason_for_id = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=ReasonType.objects.exclude(is_deleted=True),
        source="reason_for",
        write_only=True,
    )

    class Meta:
        model = Reason
        fields = "__all__"
