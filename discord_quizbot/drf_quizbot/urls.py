from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls.conf import include

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", get_schema_view(), name="coreapi-schema"),
    path("", include_docs_urls(), name="docs"),
    path("api/", include([
        path("", include("drf_quizbot.quiz.urls", namespace="quiz")),
        path("score/", include("drf_quizbot.score.urls", namespace="score")),
    ])) 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
