# coding=utf-8
from django.conf import settings
from django.db import models

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ExtraInfo(models.Model):
    """
    This model contains two extra fields that will be saved when a user registers.
    The form that wraps this model is in the forms.py file.
    """
    user = models.OneToOneField(USER_MODEL, null=True, default=None)
    support_is_donor = models.NullBooleanField(
        default=None,
    )
    support_is_periodical = models.NullBooleanField(
        default=None,
    )
    support_amount = models.DecimalField(
        null=True,
        blank=True,
        default=None,
        max_digits=5,
        decimal_places=2,
    )
    support_payment_response = models.TextField(
        null=True,
        blank=True,
        default=None,
    )
