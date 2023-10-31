from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=18, unique=True, db_index=True, verbose_name=_('phone number'))
    fullname = models.CharField(max_length=34, null=True, blank=True, verbose_name=_('fullname'))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_('is active'))
    is_ban = models.BooleanField(default=False, db_index=True, verbose_name=_('is ban'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is admin'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='auth_user_set',
        related_query_name='user',
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='auth_user_set',
        related_query_name='user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('fullname',)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.phone_number

    def is_staff(self):
        return self.is_admin
