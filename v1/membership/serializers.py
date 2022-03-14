from account.serializers import ProfileSerializer
from base.serializers import BaseSerializer
from rest_framework import serializers
from v1.membership.calculation import set_membership
from v1.wallet.serializers import TransactionCRUDSerializer
from .models import Membership, MembershipBenefits, MembershipPlain
from account.models import User


class MembershipBenefitsCRUDSerializer(BaseSerializer):
    class Meta:
        model = MembershipBenefits
        fields = "__all__"


class MembershipPlainCRUDSerializer(BaseSerializer):
    benefits = MembershipBenefitsCRUDSerializer(read_only=True, many=True)
    benefit_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=MembershipBenefits.objects.exclude(is_deleted=True),
        source="benefits",
        write_only=True,
    )
    discount_calculated = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = MembershipPlain
        fields = "__all__"


class MembershipReadOnlySerializer(BaseSerializer):
    customer = ProfileSerializer(read_only=True)
    plan = MembershipPlainCRUDSerializer(read_only=True)
    transaction = TransactionCRUDSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = "__all__"


class MembershipMutationSerializer(BaseSerializer):
    customer = ProfileSerializer(read_only=True)
    customer_id = serializers.SlugRelatedField(
        required=True,
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        source="customer",
        write_only=True,
    )
    plan = MembershipPlainCRUDSerializer(read_only=True)
    plan_id = serializers.SlugRelatedField(
        required=True,
        slug_field="id",
        queryset=MembershipPlain.objects.exclude(is_deleted=True),
        source="plan",
        write_only=True,
    )
    transaction = TransactionCRUDSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = "__all__"
        read_only_fields = (
            "amount",
            "start_at",
            "end_at",
            "is_active",
            "transaction",
            "payment_token",
        )

    def create(self, validated_data):
        instance = super(MembershipMutationSerializer, self).create(validated_data)
        #  after create membership
        membership = set_membership(instance.customer, instance.plan)
        return membership
