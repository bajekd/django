from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ["-date"]


class Category(models.Model):
    name = models.CharField(max_length=266, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name