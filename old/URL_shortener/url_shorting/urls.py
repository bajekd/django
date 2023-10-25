from django.urls import path, re_path
from django.contrib import admin

from shortener.views import HomeView, URLRedirectView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin-site'),
    path('', HomeView.as_view(), name='shortener-home'),
    path('<slug:short_code>/', URLRedirectView.as_view(),
         name='shortener-redirect'),
]

'''
    re_path(r'^(?P<short_code>[\w]{3})/$',
            URLRedirectView.as_view(), name='shortener-redirect'),
'''
