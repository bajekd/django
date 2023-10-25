from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'income'

urlpatterns = [
    path('', views.index, name="index"),
    path('add-income/', views.create_income, name='create-income'),
    path('edit-income/<int:id>', views.update_income, name='update-income'),
    path('income-delete/<int:id>', views.delete_income, name='delete-income'),
    path('search-income/', csrf_exempt(views.search_income), name='search-income'),
]