from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .managers import NotExpiredManager


User = get_user_model()


class UserLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logins', verbose_name=_('user'))
    refresh_token = models.CharField(max_length=1000, verbose_name=_('refresh_token'))
    expired_at = models.DateTimeField(verbose_name=_('expired at'))
    device_name = models.CharField(max_length=244, verbose_name=_('device name'))
    ip_address = models.GenericIPAddressField(verbose_name=_('ip address'))
    last_login = models.DateTimeField(verbose_name='last login')

    default_manager = models.Manager()
    objects = NotExpiredManager()

    class Meta:
        verbose_name = _('User Login')
        verbose_name_plural = _('User Logins')

    def __str__(self):
        return f'{self.user} - {self.device_name} - {self.ip_address}'
