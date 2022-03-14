from rest_framework import routers
from v1.payment.views import PaymentViewSet

router = routers.DefaultRouter()

app_name = "v1.payment"

router.register(r"", PaymentViewSet, basename="payment")

urlpatterns = router.urls
