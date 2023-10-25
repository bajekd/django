import pprint

from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import Room

admin.site.register(Room)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded())

    list_display = ("session_key", "session_data", "expire_date")
    exclude = ("session_data",)
    readonly_fields = ("_session_data",)
