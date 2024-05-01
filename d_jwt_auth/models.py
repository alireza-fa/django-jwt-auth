from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuth(models.Model):
    ACCESS_TOKEN = 1
    REFRESH_TOKEN = 2

    TOKEN_TYPE_CHOICES = (
        (ACCESS_TOKEN, "access token"),
        (REFRESH_TOKEN, "refresh token")
    )
    user_id = models.IntegerField(verbose_name=_("user id"), db_index=True)
    token_type = models.PositiveSmallIntegerField(choices=TOKEN_TYPE_CHOICES, verbose_name=_("token type"))
    uuid = models.UUIDField(verbose_name=_("uuid"), unique=True, db_index=True)
    device_login_count = models.PositiveSmallIntegerField(default=0, verbose_name=_("device login count"))

    class Meta:
        verbose_name = _("UserAuth")
        verbose_name_plural = _("UserAuths")
        ordering = ("-id",)

    def __str__(self):
        return f"user id: {self.user_id} - token type(a = 1, r = 2): {self.token_type} - {self.uuid}"
