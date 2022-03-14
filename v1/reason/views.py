from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets
from base.permission import ModelPermission
from v1.reason.models import Reason
from v1.reason.serializers import ReasonCRUDSerializer


class ReasonViewSet(viewsets.ModelViewSet):
    queryset = Reason.objects.exclude(is_deleted=True)
    serializer_class = ReasonCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]
