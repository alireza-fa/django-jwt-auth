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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_auths")
    token_type = models.PositiveSmallIntegerField(choices=TOKEN_TYPE_CHOICES, verbose_name=_("token type"))
    uuid = models.UUIDField(verbose_name=_("uuid"), unique=True)

    class Meta:
        verbose_name = _("UserAuth")
        verbose_name_plural = _("UserAuths")

    def __str__(self):
        return f"{self.user} - token type(a = 1, r = 2): {self.token_type}"
