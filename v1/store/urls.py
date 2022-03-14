from rest_framework import routers

from v1.store.views import StoreViewSet

router = routers.DefaultRouter()

app_name = "v1.store"

router.register(r"", StoreViewSet, basename="store")

urlpatterns = router.urls
