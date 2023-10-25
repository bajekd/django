from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=266)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ["-date"]


class Source(models.Model):
    name = models.CharField(max_length=266, unique=True)

    def __str__(self):
        return self.name
