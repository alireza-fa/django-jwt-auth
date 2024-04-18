import functools
from datetime import timedelta
from Crypto.Random import get_random_bytes

from .client import IP_ADDRESS, DEVICE_NAME


class AppSettings:

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def _setting(self, name: str, default: object):
        from django.conf import settings
        return getattr(settings, self.prefix + name, default)

    @property
    def access_token_lifetime_minutes(self):
        return self._setting("ACCESS_TOKEN_LIFETIME_MINUTES", timedelta(minutes=10))

    @property
    def refresh_token_lifetime_days(self):
        return self._setting("REFRESH_TOKEN_LIFETIME_DAYS", timedelta(days=30))

    @property
    def refresh_token_claims(self):
        return {
            **self._setting("REFRESH_TOKEN_CLAIMS", {"id": 0}),
            "id": 0,
            IP_ADDRESS: "",
            DEVICE_NAME: "",
        }

    @property
    def access_token_claims(self):
        return {
            **self._setting("ACCESS_TOKEN_CLAIMS", {"id": 0}),
            "id": 0,
            IP_ADDRESS: "",
            DEVICE_NAME: "",
        }

    @property
    def access_token_user_field_claims(self):
        return self._setting("ACCESS_TOKEN_USER_FIELD_CLAIMS", {"id": 0})

    @property
    def encrypt_key(self):
        return self._setting("ENCRYPT_KEY", get_random_bytes(32))


@functools.lru_cache
def jwt_auth_app_settings() -> AppSettings:
    return AppSettings("JWT_AUTH_")


app_setting = jwt_auth_app_settings()
