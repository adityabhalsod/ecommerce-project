from django.apps import AppConfig


class DeliveryConfig(AppConfig):
    name = "v1.delivery"
    verbose_name = "Delivery"

    def ready(self):
        import v1.delivery.signals  # no qa
