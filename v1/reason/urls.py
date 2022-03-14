from rest_framework import routers

from v1.reason.views import ReasonViewSet

router = routers.DefaultRouter()

app_name = "v1.reason"

router.register(r"", ReasonViewSet, basename="reason")

urlpatterns = router.urls
