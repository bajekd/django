import debug_toolbar
from django_otp.admin import OTPAdminSite
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("unexpected_admin/", admin.site.urls),
    path("", include("ecommerce.apps.catalogue.urls", namespace="catalogue")),
    path("basket/", include("ecommerce.apps.basket.urls", namespace="basket")),
    path("account/", include("ecommerce.apps.account.urls", namespace="account")),
    path("checkout/", include("ecommerce.apps.checkout.urls", namespace="checkout")),
    path("orders/", include("ecommerce.apps.orders.urls", namespace="orders")),
    path("__debug__/", include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.__class__ = OTPAdminSite
admin.site.site_header = "Ecommerce Admin"
