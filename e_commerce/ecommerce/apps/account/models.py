import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomAccountManager(BaseUserManager):
    def validate_email_(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address!"))

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True!")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True!")
        if other_fields.get("is_active") is not True:
            raise ValueError("Superuser must be assigned to is_active=True!")

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if email:
            email = self.normalize_email(email)
            self.validate_email_(email)
        else:
            raise ValueError(_("You must provide an email address!"))

        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()

        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email adress"), unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(blank=True, max_length=18)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("name",)

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(subject, message, "admin@admin.com", [self.email], fail_silently=False)

    def __str__(self):
        return self.name


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone_number = models.CharField(_("Phone Number"), max_length=18)
    address_line = models.CharField(_("Address Line"), max_length=256)
    town_city = models.CharField(_("Town/City/State"), max_length=120)
    postal_code = models.CharField(_("Postcode"), max_length=12)
    delivery_instructions = models.CharField(_("Delivery Instructions"), blank=True, null=True, max_length=256)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return f"{self.full_name} Address"
