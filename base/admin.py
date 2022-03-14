from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin


class BaseAdmin(LeafletGeoAdmin):
    def __init__(self, model, admin_site):
        self.readonly_fields = self.readonly_fields + (
            "created_at",
            "updated_at",
            "is_deleted",
        )
        self.list_per_page = 25
        self.list_max_show_all = 100
        super().__init__(model, admin_site)


class BaseModelAdmin(admin.StackedInline):
    def __init__(self, parent_model, admin_site):
        self.readonly_fields = self.readonly_fields + (
            "created_at",
            "updated_at",
            "is_deleted",
        )
        self.list_per_page = 25
        self.list_max_show_all = 100
        super().__init__(parent_model, admin_site)
