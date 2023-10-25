from django.contrib import admin
from .models import Expense, Category

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'date',)
    search_fields = ('description', 'date',)
    list_editable = ('description', 'owner','date',)
    list_filter = ('category',)
    list_per_page = 10

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)