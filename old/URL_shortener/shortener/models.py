from django.conf import settings
from django.db import models
from .utilis import create_shortcode
from .validators import validate_url

SHORT_CODE_LENGTH = getattr(settings, "SHORT_CODE_LENGTH", 3)


# Create your models here.


class ShortenerURL(models.Model):
    url = models.CharField(max_length=250, validators=[validate_url])
    short_code = models.CharField(
        max_length=SHORT_CODE_LENGTH, unique=True, blank=True)
    count = models.IntegerField(default=0)
    # every time when model is saved
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.url)} --> {str(self.short_code)}'

    def save(self, *args, **kwargs):
        if self.short_code is None or self.short_code == '':
            self.short_code = create_shortcode(self)
        super(ShortenerURL, self).save(*args, **kwargs)
