from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import BaseUserManager


class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, verbose_name=_('username'), unique=True)
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('phone number'))
    email = models.EmailField(max_length=64, verbose_name=_("email"), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is admin'))

    objects = BaseUserManager()

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ("username",)

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
