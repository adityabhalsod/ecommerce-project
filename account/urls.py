from rest_framework import routers

from account.views import (
    AddressViewSet,
    AuthenticationViewSet,
    GroupReadOnlyViewSet,
    GroupViewSet,
    PermissionViewSet,
    ProfileViewSet,
    UserPhotosViewSet,
)

router = routers.DefaultRouter()

app_name = "account"

router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"photo", UserPhotosViewSet, basename="photo")
router.register(r"permission", PermissionViewSet, basename="permission")
router.register(r"group/read-only", GroupReadOnlyViewSet, basename="group-read-only")
router.register(r"group", GroupViewSet, basename="group")
router.register(r"address", AddressViewSet, basename="address")
router.register(r"", AuthenticationViewSet, basename="account")

urlpatterns = router.urls
