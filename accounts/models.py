from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import BaseUserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(BaseModel):
    IMAGE = 1
    MOVIE = 2
    PDF = 3

    FILE_TYPE_CHOICES = (
        (IMAGE, _("image")),
        (MOVIE, _("Movie")),
        (PDF, _("pdf")),
    )

    file_type = models.PositiveSmallIntegerField(choices=FILE_TYPE_CHOICES, verbose_name=_("file type"))
    filename = models.CharField(max_length=64, verbose_name=_("filename"), unique=True, db_index=True)
    size = models.IntegerField(verbose_name=_("size"))

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self):
        return f"{self.file_type} - {self.filename}"


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=64, verbose_name=_("fullname"), db_index=True)
    national_code = models.CharField(max_length=10, verbose_name=_("national code"), db_index=True)
    phone_number = models.CharField(max_length=16,  verbose_name=_("phone number"), db_index=True, unique=True)
    email = models.EmailField(max_length=120, verbose_name=_("email"), null=True, blank=True, unique=True)
    verified_email = models.BooleanField(default=False, verbose_name=_("verified email"))
    avatar_image = models.OneToOneField(
        File, verbose_name=_("avatar image"), related_name="user_avatar_image",
        on_delete=models.CASCADE, null=True, blank=True)
    last_image_update = models.DateTimeField(verbose_name=_("last image update"), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    is_admin = models.BooleanField(default=False, verbose_name=_("is admin"))

    objects = BaseUserManager()

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ('fullname', 'email', 'national_code')

    def __str__(self):
        return self.fullname

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserRole(BaseModel):
    DEFAULT = 1
    ADMIN = 2
    DOCTOR = 3
    SHOP = 4
    COACH = 5

    ROLE_CHOICES = (
        (DEFAULT, _("default")),
        (ADMIN, _("admin")),
        (DOCTOR, _("doctor")),
    )

    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='roles', verbose_name=_('user'))
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, verbose_name=_("role"))

    def __str__(self):
        return f'{self.user} - {self.role}'

    class Meta:
        verbose_name = _("User role")
        verbose_name_plural = _("User roles")
        unique_together = [["user", "role"]]
