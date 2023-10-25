from django.urls import path

from .views import RandomQuestion

app_name = "quiz"

urlpatterns = [
    path("random/", RandomQuestion.as_view(), name="random_question"),
]
