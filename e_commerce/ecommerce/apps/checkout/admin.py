from django.contrib import admin

from .models import DeliveryOptions, PaymentSelections

# Register your models here.

admin.site.register(DeliveryOptions)
admin.site.register(PaymentSelections)
