from django.db import models
from django.db.models.base import Model
from django.urls import reverse

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = models.CharField(max_length=256)
    long_description = models.TextField(blank=True, null=True)
    technology = models.CharField(max_length=255)
    link_to_repo = models.CharField(max_length=150)
    image = models.FilePathField(path="media/img/")
    gif = models.FileField(upload_to="gifs/", max_length=100, blank=True)
    ordering = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("ordering",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={"slug": self.slug})
