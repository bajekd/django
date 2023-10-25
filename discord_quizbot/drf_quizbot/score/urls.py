from django.urls import path

from .views import Leaderboard, UpdateScore

app_name = "score"

urlpatterns = [
    path("update/", UpdateScore.as_view(), name="random_question"),
    path("leaderboard/", Leaderboard.as_view(), name="leaderboard"),
]
