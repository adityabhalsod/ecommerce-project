from django.apps import AppConfig


class WalletConfig(AppConfig):
    name = "v1.wallet"
    verbose_name = "Wallet"

    def ready(self):
        import v1.wallet.signals  # no qa
