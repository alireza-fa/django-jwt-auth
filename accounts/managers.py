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
            fullname: str,
            email: str | None = None,
            password: str = generate_password(),
    ):
        if phone_number is None:
            raise ValueError(_('User must have phone number'))
        elif password is None:
            raise ValueError(_('User must have password'))

        user = self.model(
            phone_number=phone_number,
            fullname=fullname,
        )
        if email:
            user.email = BaseUserManager.normalize_email(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(
            self,
            phone_number: str,
            fullname: str,
            email: str | None = None,
            password: str = generate_password(),
    ):
        user = self.create_user(
            phone_number=phone_number,
            fullname=fullname,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            phone_number: str,
            fullname: str,
            email: str | None = None,
            password: str = generate_password(),
    ):
        user = self.create_admin(
            phone_number=phone_number,
            fullname=fullname,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user
