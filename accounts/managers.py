from django.contrib.auth.models import BaseUserManager as BaseManager


class BaseUserManager(BaseManager):

    def create_user(
            self, fullname: str, national_code: str, phone_number: str,
            email: str | None = None, is_active: bool = True, is_admin: bool = False,
            is_superuser: bool = False, password: str | None = None) -> object:
        if not fullname:
            raise ValueError("Users must have an fullname")
        if not national_code:
            raise ValueError("Users must have an national_code")
        if not phone_number:
            raise ValueError("Users must have an phone_number")

        user = self.model(
            fullname=fullname,
            national_code=national_code,
            phone_number=phone_number,
            email=None if email is None else BaseManager.normalize_email(email),
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password(password)

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_admin(
            self, fullname: str, national_code: str, phone_number: str,
            email: str | None = None, is_active: bool = True, is_admin: bool = True,
            is_superuser: bool = False, password: str | None = None) -> object:
        user = self.create_user(
            fullname=fullname,
            national_code=national_code,
            phone_number=phone_number,
            email=email,
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser,
            password=password
        )
        return user

    def create_superuser(
            self, fullname: str, national_code: str, phone_number: str,
            email: str | None = None, is_active: bool = True, is_admin: bool = True,
            is_superuser: bool = True, password: str | None = None) -> object:
        user = self.create_user(
            fullname=fullname,
            national_code=national_code,
            phone_number=phone_number,
            email=email,
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser,
            password=password
        )
        return user

    def get_queryset(self):
        return super().get_queryset().prefetch_related("roles")
