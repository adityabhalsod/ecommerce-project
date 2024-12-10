from rest_framework import routers
from v1.promotion.views import (
    DiscountVoucherMutationViewSet,
    DiscountVoucherViewSet,
    ReferralAndEarnViewSet,
)

router = routers.DefaultRouter()

app_name = "v1.promotion"

router.register(
    r"discount-voucher", DiscountVoucherViewSet, basename="discount-voucher"
)
router.register(
    r"discount-voucher-mutation",
    DiscountVoucherMutationViewSet,
    basename="discount-voucher-mutation",
)
router.register(
    r"referral-and-earn",
    ReferralAndEarnViewSet,
    basename="referral-and-earn",
)


urlpatterns = router.urls
