from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

from . import views
from .forms import UserLoginForm

app_name = "account"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login.html", form_class=UserLoginForm),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="account:login"), name="logout"),
    path("register/", views.account_register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>", views.account_activate, name="activate"),
    path("dashboard/", views.account_dashboard, name="dashboard"),
    path(
        "profile/",
        include(
            [
                path("edit/", views.edit_details, name="edit_details"),
                path("delete_user/", views.delete_user, name="delete_user"),
                path(
                    "delete_confirm/",
                    TemplateView.as_view(template_name="account/delete_confirm.html"),
                    name="delete_confirmation",
                ),
            ]
        ),
    ),
    path(
        "addresses/",
        include(
            [
                path("", views.view_address, name="addresses"),
                path("add/", views.add_address, name="add_address"),
                path("edit/<slug:id>", views.edit_address, name="edit_address"),
                path("delete/<slug:id>", views.delete_address, name="delete_address"),
                path("set_default/<slug:id>/", views.set_default, name="set_default_address"),
            ]
        ),
    ),
    path("orders/", views.orders_dashboard, name="orders"),
    path(
        "wishlist/",
        include(
            [
                path("", views.wishlist_dashboard, name="wishlist"),
                path("wishlist/modify/<int:id>", views.modify_wishlist, name="modify_wishlist"),
            ]
        ),
    ),
]
