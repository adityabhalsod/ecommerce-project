from rest_framework import routers

from v1.wallet.views import (
    CustomerWalletViewSet,
    DeliveryBoyWalletViewSet,
    TransactionViewSet,
    CaseOnDeliveryCollectionHistoryViewSet,
)

router = routers.DefaultRouter()

app_name = "v1.wallet"

router.register(r"customer-wallet", CustomerWalletViewSet, basename="customer-wallet")
router.register(
    r"delivery-boy-wallet", DeliveryBoyWalletViewSet, basename="delivery-boy-wallet"
)
router.register(
    r"delivery-boy-transaction",
    CaseOnDeliveryCollectionHistoryViewSet,
    basename="delivery-boy-transaction",
)
router.register(r"transaction", TransactionViewSet, basename="transaction")

urlpatterns = router.urls
