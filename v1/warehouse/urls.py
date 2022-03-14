from rest_framework import routers
from v1.warehouse.views import (
    PurchaseViewSet,
    StockTransferViewSet,
    StoreStockManagementViewSet,
    SupplierViewSet,
    WarehouseStockManagementViewSet,
    WarehouseViewSet,
)

router = routers.DefaultRouter()

app_name = "v1.warehouse"

router.register(r"purchase", PurchaseViewSet, basename="purchase")
router.register(r"stock-transfer", StockTransferViewSet, basename="StockTransfer")
router.register(r"warehouse", WarehouseViewSet, basename="warehouse")
router.register(r"supplier", SupplierViewSet, basename="supplier")
router.register(
    r"store-stock-management",
    StoreStockManagementViewSet,
    basename="store-stock-management",
)
router.register(
    r"warehouse-stock-management",
    WarehouseStockManagementViewSet,
    basename="warehouse-stock-management",
)


urlpatterns = router.urls
