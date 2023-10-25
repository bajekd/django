from django.db import models
from django.utils.translation import ugettext as _


class Score(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    points = models.IntegerField(_("Points"))

    def __str__(self):
        return self.name
