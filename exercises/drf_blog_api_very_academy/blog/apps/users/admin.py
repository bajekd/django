from django.contrib import admin
from django.contrib.auth import get_user_model


class UserAdmin(admin.ModelAdmin):
    search_fields = ("id", "email",)
    list_display = ('id', "email",)
    list_editable = 'email',
    list_filter = ('is_staff',)
    ordering = '-start_date',


admin.site.register(get_user_model(), UserAdmin)
