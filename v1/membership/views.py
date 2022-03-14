from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import mixins, viewsets
from v1.membership.models import Membership, MembershipPlain
from base.permission import ModelPermission
from v1.membership.serializers import (
    MembershipMutationSerializer,
    MembershipReadOnlySerializer,
    MembershipPlainCRUDSerializer,
)


class MembershipViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Membership.objects.exclude(is_deleted=True)
    serializer_class = MembershipReadOnlySerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = [
        "is_active",
    ]
    ordering_fields = [
        "start_at",
        "end_at",
    ]
    permission_classes = [ModelPermission]

    def get_serializer_class(self):
        if self.action == "create":
            return MembershipMutationSerializer
        return self.serializer_class


class MembershipPlainViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlain.objects.exclude(is_deleted=True)
    serializer_class = MembershipPlainCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = [
        "type",
        "is_active",
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]
