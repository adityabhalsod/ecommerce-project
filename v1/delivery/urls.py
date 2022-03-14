from rest_framework import routers
from v1.delivery.views import (
    DeliveryBoyDocumentViewSet,
    DeliveryBoyReviewViewSet,
    DeliveryBoyVehicleInformationViewSet,
    DeliveryBoyVehiclePhotosViewSet,
    DeliveryChargesViewSet,
    DeliveryPayoutViewSet,
    DeliveryViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()

app_name = "v1.delivery"

router.register(r"order", OrderViewSet, basename="order")
router.register(r"profile", DeliveryViewSet, basename="profile")
router.register(r"charge", DeliveryChargesViewSet, basename="charge")
router.register(r"payout", DeliveryPayoutViewSet, basename="payout")
router.register(r"document", DeliveryBoyDocumentViewSet, basename="document")
router.register(r"review", DeliveryBoyReviewViewSet, basename="review")
router.register(
    r"vehicle-information",
    DeliveryBoyVehicleInformationViewSet,
    basename="vehicle-information",
)
router.register(
    r"vehicle-photos",
    DeliveryBoyVehiclePhotosViewSet,
    basename="vehicle-photos",
)

urlpatterns = router.urls
