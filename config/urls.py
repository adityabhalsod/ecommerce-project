"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from .documentation import documentation_url

from django.contrib.admin import site
import adminactions.actions as actions

# register all adminactions
actions.add_to_site(site)

# from django_otp.admin import OTPAdminSite
# admin.site.__class__ = OTPAdminSite


urlpatterns = (
    [
        path("quickly/super-admin/", admin.site.urls),
        path("quickly/super-admin/postgres-metrics/", include("postgres_metrics.urls")),
        path("quickly/super-admin/adminactions/", include("adminactions.urls")),
        path("ckeditor/", include("ckeditor_uploader.urls")),
        path("api/v1/account/", include("account.urls", namespace="account")),
        path("api/v1/catelog/", include("v1.catalog.urls", namespace="catalog")),
        path("api/v1/cart/", include("v1.cart.urls", namespace="cart")),
        path("api/v1/delivery/", include("v1.delivery.urls", namespace="delivery")),
        path("api/v1/group/", include("v1.group.urls", namespace="group")),
        path(
            "api/v1/membership/",
            include("v1.membership.urls", namespace="membership"),
        ),
        path("api/v1/store/", include("v1.store.urls", namespace="store")),
        path("api/v1/order/", include("v1.orders.urls", namespace="order")),
        path("api/v1/payment/", include("v1.payment.urls", namespace="payment")),
        path("api/v1/package/", include("v1.package.urls", namespace="package")),
        path("api/v1/promotion/", include("v1.promotion.urls", namespace="promotion")),
        path("api/v1/warehouse/", include("v1.warehouse.urls", namespace="warehouse")),
        path("api/v1/wallet/", include("v1.wallet.urls", namespace="wallet")),
        path(
            "robots.txt",
            TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + documentation_url
)


# path("api/v1/reason/", include("v1.reason.urls", namespace="reason")),
