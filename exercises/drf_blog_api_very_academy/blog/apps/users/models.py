from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def validate_email_(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address!"))

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have assigned is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have assigned is_superuser=True")
        if other_fields.get("is_active") is not True:
            raise ValueError("Superuser must have assigned is_active=True")

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if email:
            email = self.normalize_email(email)
            self.validate_email_(email)
        else:
            raise ValueError(_("You must provide email adress!"))

        
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_("about"), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
