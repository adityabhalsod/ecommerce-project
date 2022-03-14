from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = "v1.orders"
    verbose_name = "Orders"

    def ready(self):
        import v1.orders.signals  # no qa
