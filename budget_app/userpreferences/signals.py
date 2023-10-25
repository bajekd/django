from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserPreference


@receiver(post_save, sender=User)
def create_userpreferences(sender, instance, created, **kwargs):
    if created:
        UserPreference.objects.create(user=instance)


"""
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
      UserPreference.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
"""
