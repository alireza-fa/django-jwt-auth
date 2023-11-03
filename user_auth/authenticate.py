from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken

from .encryption import decrypt


class CustomAuthentication(JWTAuthentication):

    def get_validated_token(self, raw_token: bytes) -> Token:
        try:
            token = decrypt(encrypted=raw_token)
        except ValueError:
            raise InvalidToken(
                {
                    "detail": _("Given token not valid for any token type"),
                }
            )
        return super().get_validated_token(token.encode())
