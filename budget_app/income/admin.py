from django.contrib import admin
from .models import Income, Source

# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'date',)
    search_fields = ('description', 'date',)
    list_editable = ('description', 'owner','date',)
    list_filter = ('source',)
    list_per_page = 10

  
admin.site.register(Income, IncomeAdmin)
admin.site.register(Source)