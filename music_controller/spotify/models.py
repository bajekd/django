from django.db import models
from django.utils.translation import ugettext_lazy as _


class SpotifyToken(models.Model):
    user = models.CharField(_("User session id"), max_length=75, unique=True)
    token_type = models.CharField(_("Token Type"), max_length=50)
    refresh_token = models.CharField(_("Refresh Token"), max_length=75)
    access_token = models.CharField(_("Access Token"), max_length=75)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    expires_in = models.DateTimeField(_("Expiration Date"))

    def __str__(self):
        return self.expires_in.strftime("%Y/%m/%d, %H:%M:%S")


class Vote(models.Model):
    user = models.CharField(_("User session id"), max_length=75, unique=True)
    room = models.ForeignKey(
        "api.Room", verbose_name=_("Forein key to room"), related_name="votes", on_delete=models.CASCADE
    )
    song_id = models.CharField(_("Song"), max_length=50)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return self.song_id
