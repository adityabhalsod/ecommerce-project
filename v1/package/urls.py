from rest_framework import routers
from v1.package.views import PackageBoyViewSet, OrderViewSet

router = routers.DefaultRouter()

app_name = "v1.package"

router.register(r"order", OrderViewSet, basename="order")
router.register(r"", PackageBoyViewSet, basename="package")

urlpatterns = router.urls
