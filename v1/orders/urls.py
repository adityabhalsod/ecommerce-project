from rest_framework import routers

from v1.orders.views import OrderViewSet

router = routers.DefaultRouter()

app_name = "v1.orders"

router.register(r"", OrderViewSet, basename="order")

urlpatterns = router.urls
