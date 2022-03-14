from django.apps import AppConfig


class WarehouseConfig(AppConfig):
    name = "v1.warehouse"
    verbose_name = "Warehouse"

    def ready(self):
        import v1.warehouse.signals  # no qa
