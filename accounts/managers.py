from django.contrib.auth.models import BaseUserManager as BaseManager


class BaseUserManager(BaseManager):

    def create_user(self, username, phone_number, email=None,
                    is_active=True, is_admin=False, is_superuser=False, password=None):
        if not username:
            raise ValueError('Users must have an fullname')
        if not phone_number:
            raise ValueError('Users must have an phone_number')

        user = self.model(
            username=username,
            phone_number=phone_number,
            email=BaseManager.normalize_email(email),
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_admin(self, username, phone_number, email=None,
                     is_active=True, is_admin=True, is_superuser=False, password=None):
        user = self.create_user(
            username=username,
            phone_number=phone_number,
            email=BaseManager.normalize_email(email),
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser,
            password=password,
        )
        return user

    def create_superuser(self, username, phone_number, email=None,
                         is_active=True, is_admin=True, is_superuser=True, password=None):
        user = self.create_user(
            username=username,
            phone_number=phone_number,
            email=BaseManager.normalize_email(email),
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser,
            password=password,
        )
        return user
