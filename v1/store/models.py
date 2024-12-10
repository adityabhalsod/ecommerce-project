from django.contrib.gis.db import models
from django.db.models import Max
from django.template.defaultfilters import slugify
from django.utils.encoding import force_str
from base import google_map
from base.models import BaseModel


class Store(BaseModel):
    manager = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="store_manager",
    )
    address = models.TextField(default="", null=True, blank=True)
    geo_location = models.PointField(srid=4326, default=None, null=True, blank=True)
    store_number = models.BigIntegerField(default=0, null=True, blank=True)
    store_name = models.CharField(default="", max_length=255, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    pin_code = models.CharField(max_length=16, null=True, blank=True)
    allow_geo_location_path = models.MultiPolygonField(srid=4326, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)
    is_address_set_manually = models.BooleanField(default=False)
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    delivery_time = models.CharField(default="", max_length=255, blank=True, null=True)
    slug = models.CharField(default="", max_length=255, blank=True, null=True)
    warehouse = models.ForeignKey(
        "warehouse.Warehouse",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "store"
        unique_together = [("store_name",)]

    def save(self, *args, **kwargs):
        self.slug = slugify(force_str(self.store_name))

        if self._state.adding:
            # Current count
            current_count = (
                self.__class__.objects.aggregate(Max("store_number")).get(
                    "store_number__max"
                )
                or 0
            )

            if len(str(current_count)) < 3:
                current_count = current_count + 100

            # store_number
            self.store_number = current_count + 1

        if (
            not self.is_address_set_manually
            and self.geo_location
            and self.geo_location.coords
        ):
            gep_code = google_map.GeoCode(coordinated=self.geo_location.coords)
            geo_coded_address = gep_code.reverse_geocode()
            if geo_coded_address:
                self.address = geo_coded_address.address
                self.city = geo_coded_address.city
                self.state = geo_coded_address.state
                self.pin_code = geo_coded_address.pin_code
        return super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.store_name)
