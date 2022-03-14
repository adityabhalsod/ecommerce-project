from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets
from base.permission import ModelPermission
from v1.store.models import Store
from v1.store.serializers import StoreCRUDSerializer
from django.contrib.gis.geos import Point


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.exclude(is_deleted=True)
    serializer_class = StoreCRUDSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [ModelPermission]

    def get_queryset(self):
        queryset = self.queryset
        lat = self.request.query_params.get("lat", 0.0)
        long = self.request.query_params.get("long", 0.0)
        if lat and long:
            queryset = self.queryset.filter(
                allow_geo_location_path__contains=Point(float(lat), float(long))
            )
        return self.filter_queryset(queryset)
