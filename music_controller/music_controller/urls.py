from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", get_schema_view(), name="coreapi-schema"),
    path("docs/", include_docs_urls(), name="docs"),
    path("api/", include("api.urls", namespace="api")),
    path("spotify/", include("spotify.urls", namespace="sporify")),
    path("", include("frontend.urls", namespace="frontend")),
]
