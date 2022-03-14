from rest_framework import routers

from v1.group.views import (
    GroupTypeViewSet,
    ColorViewSet,
    GroupStructureViewSet,
    CollectionViewSet,
    MultiplePhotosViewSet,
    ProductCollectionViewSet,
    GroupStructureAdminViewSet,
)

router = routers.DefaultRouter()

app_name = "v1.group"

router.register(r"type", GroupTypeViewSet, basename="type")
router.register(r"color", ColorViewSet, basename="color")
router.register(
    r"structure-admin", GroupStructureAdminViewSet, basename="structure-admin"
)
router.register(r"structure", GroupStructureViewSet, basename="structure")
router.register(r"multiple-photos", MultiplePhotosViewSet, basename="multiple-photos")
router.register(r"collection", CollectionViewSet, basename="collection")
router.register(
    r"product-collection", ProductCollectionViewSet, basename="product-collection"
)

urlpatterns = router.urls
