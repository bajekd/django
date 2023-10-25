from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path("api/", include([
        path("", include("blog.apps.blog_api.urls", namespace="blog_api")),
        path("user/", include("blog.apps.users.urls", namespace="users")),
        path('token/', include([
            path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        ])),
    ])),
    path("", include("blog.apps.blog.urls", namespace="blog")),
    path("admin/", admin.site.urls),
    path("schema/", get_schema_view(), name="coreapi-schema"),
    path("docs/", include_docs_urls, name="docs"),
]
