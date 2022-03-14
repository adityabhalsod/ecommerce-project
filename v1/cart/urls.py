from rest_framework import routers

from v1.cart.views import CartViewSet, CheckoutViewSet

router = routers.DefaultRouter()

app_name = "v1.cart"

router.register(r"checkout", CheckoutViewSet, basename="checkout")
router.register(r"", CartViewSet, basename="cart")


urlpatterns = router.urls
