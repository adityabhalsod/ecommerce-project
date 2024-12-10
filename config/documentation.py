"""Handle all documentation related functions."""
import os

from django.conf import settings
from django.urls import re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="{} API".format(settings.PROJECT_NAME),
        default_version=os.getenv("PROJECT_VERSION", "V1"),
        description=os.getenv("PROJECT_DESCRIPTION", "No description."),
        terms_of_service="https://policies.google.com/terms",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

documentation_url = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
