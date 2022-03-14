from rest_framework import routers

from v1.membership.views import MembershipPlainViewSet, MembershipViewSet

router = routers.DefaultRouter()

app_name = "v1.membership"


router.register(r"plan", MembershipPlainViewSet, basename="plan")
router.register(r"", MembershipViewSet, basename="membership")


urlpatterns = router.urls
