from django.conf import settings
from django.db import models
from django.db.models.fields import related
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=225)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=225, unique_for_date="published")
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=options, default="published")
    objects = models.Manager()  # default manager
    PostObjects = PostObjects()  # custom manager

    class Meta:
        ordering = ("-published",)

    def __str__(self):
        return self.title
