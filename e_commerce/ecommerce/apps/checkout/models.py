from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class DeliveryOptions(models.Model):
    DELIVERY_CHOICES = (
        ("IS", "In store"),
        ("HD", "Home delivery"),
        ("DD", "Digital delivery"),
    )

    delivery_name = models.CharField(verbose_name=_("delivery name"), help_text=_("Required"), max_length=255)
    delivery_price = models.DecimalField(
        verbose_name=_("delivery price"),
        help_text=_("Maximum 99999.99"),
        max_digits=7,
        decimal_places=2,
        error_messages={"name": {"max_length": _("The price must be between 0 and 99999.99")}},
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES, verbose_name=_("delivery_method"), help_text=_("Required"), max_length=255
    )
    delivery_timeframe = models.CharField(
        verbose_name=_("delivery timeframe"), help_text=_("Required"), max_length=255
    )
    delivery_window = models.CharField(verbose_name=_("delivery window"), help_text=_("Required"), max_length=255)
    order = models.IntegerField(verbose_name=_("list order"), help_text=_("Required"), default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")
        ordering = ("order",)

    def __str__(self):
        return self.delivery_name


class PaymentSelections(models.Model):
    name = models.CharField(verbose_name=_("name"), help_text=_("Required"), max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self):
        return self.name
