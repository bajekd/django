from . import views
from django.urls import path

app_name = "preferences"

urlpatterns = [
  path('', views.index, name='index'),
]
