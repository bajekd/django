from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Item(models.Model):
    owner = models.ForeignKey(
        User, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    description = models.TextField()
    image_url = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name
