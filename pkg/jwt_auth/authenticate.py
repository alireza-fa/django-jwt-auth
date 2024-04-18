from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken

from pkg.jwt_auth.encrypto.encryption import decrypt
from .token import get_user_by_access_token


User = get_user_model()


class JWTAuthentication(BaseJWTAuthentication):

    def get_validated_token(self, raw_token: bytes) -> Token:
        try:
            token = decrypt(encrypted=raw_token, key=settings.ENCRYPT_KEY)
        except ValueError:
            raise InvalidToken(
                {
                    "detail": _("Given token not valid for any token type"),
                }
            )
        return super().get_validated_token(token.encode())

    def get_user(self, validated_token: Token) -> AuthUser:
        return get_user_by_access_token(token=validated_token)
