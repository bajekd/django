from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    #
    path("", views.dashboard, name="accounts-dashboard"),
    path("user/", views.user_page, name="user_page"),
    path("products/", views.products, name="accounts-products"),
    path("customer/<int:pk>", views.customer, name="accounts-customer"),
    #
    path("create_order/<int:customer_pk>", views.create_order, name="create-order"),
    path("update_order/<int:pk>", views.update_order, name="update-order"),
    path("delete_order/<int:pk>", views.delete_order, name="delete-order"),
]
