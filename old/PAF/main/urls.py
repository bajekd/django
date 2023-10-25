from django.urls import path
from main import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('items/', views.itemspage, name='items'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
]
