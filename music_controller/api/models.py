from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utilis import generate_unique_room_code


class Room(models.Model):
    room_code = models.CharField(
        _("Room Code"),
        max_length=getattr(settings, "ROOM_CODE_LENGTH", 24),
        default=generate_unique_room_code,
        unique=True,
    )
    host = models.CharField(_("Host code"), max_length=75, unique=True)
    guest_can_pause = models.BooleanField(_("Gues can pause permission"), default=False)
    votes_to_skip = models.IntegerField(_("Votes to skip"), default=1)
    current_song = models.CharField(_("Current song"), max_length=50, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return self.host
