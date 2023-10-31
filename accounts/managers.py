from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Manager
from django.utils import timezone

from string import digits, ascii_letters, punctuation
from random import choices


def generate_password(pattern: str = digits + ascii_letters + punctuation, k: int = 12):
    return ''.join(choices(pattern, k=k))


class UserManager(BaseUserManager):

    def create_user(
            self,
            phone_number: str,
            password: str = generate_password(),
            fullname: str | None = None,
    ):
        if phone_number is None:
            raise ValueError(_('User must have phone number'))
        elif password is None:
            raise ValueError(_('User must have password'))

        user = self.model(
            phone_number=phone_number,
            fullname=fullname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(
            self,
            phone_number: str,
            password: str = generate_password(),
            fullname: str | None = None,
    ):
        user = self.create_user(
            phone_number=phone_number,
            fullname=fullname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            phone_number: str,
            password: str = generate_password(),
            fullname: str | None = None,
    ):
        user = self.create_admin(
            phone_number=phone_number,
            fullname=fullname,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class NotExpiredActiveManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(expired_at__gt=timezone.now(), is_active=True)


class NotExpiredManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(expired_at__gt=timezone.now())
