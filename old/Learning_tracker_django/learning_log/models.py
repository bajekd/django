from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    """A topic the user is learning about"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) # see line 22

    def __str__(self):
        """Return a string representation of the model"""
        return self.text


class Entry(models.Model):
    """Something specific learned about a topic"""
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # This tells Django that when
    # a topic is deleted,all of the entries in that topic should be deleted as well.

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model """
        if len(self.text) > 50:
            return self.text[:50] + "..."
        else:
            return self.text[:50]