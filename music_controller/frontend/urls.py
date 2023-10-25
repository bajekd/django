from django.urls import include, path

from .views import index, room

app_name = "frontend"

urlpatterns = [
    path("", index, name="home"),
    path("create/", index),
    path("join/", index),
    path("room/<str:roomCode>/", room)
]