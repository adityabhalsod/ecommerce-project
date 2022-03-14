from rest_framework import routers

from v1.catalog.views import (
    CategoryViewSet,
    ProductPhotoViewSet,
    ProductSearchViewSet,
    ProductViewSet,
    ProductStockMasterViewSet,
    UnitViewSet,
    VariationPhotoViewSet,
)

router = routers.DefaultRouter()

app_name = "v1.catalog"

router.register(r"category", CategoryViewSet, basename="category")
router.register(r"product-photos", ProductPhotoViewSet, basename="product-photos")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"master", ProductStockMasterViewSet, basename="master")
router.register(r"variation-photos", VariationPhotoViewSet, basename="variation-photos")
router.register(r"unit", UnitViewSet, basename="unit")
router.register(r"search", ProductSearchViewSet, basename="search")

urlpatterns = router.urls
