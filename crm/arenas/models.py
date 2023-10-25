from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.


class Location(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=275, unique=True)

    def __str__(self):
        return self.identifier