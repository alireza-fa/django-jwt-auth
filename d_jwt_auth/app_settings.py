import functools
from datetime import timedelta
from Crypto.Random import get_random_bytes

from .client import IP_ADDRESS, DEVICE_NAME
from .constants import USER_ID, UUID_FIELD


class AppSettings:

    def __init__(self, prefix: str, encryption_key: bytes) -> None:
        self.prefix = prefix
        self.encryption_key = encryption_key

    def _setting(self, name: str, default: object):
        from django.conf import settings
        return getattr(settings, self.prefix + name, default)

    @property
    def access_token_lifetime(self):
        return self._setting("ACCESS_TOKEN_LIFETIME", timedelta(minutes=10))

    @property
    def refresh_token_lifetime(self):
        return self._setting("REFRESH_TOKEN_LIFETIME", timedelta(days=30))

    @property
    def refresh_token_claims(self):
        return {
            **self._setting("REFRESH_TOKEN_CLAIMS", {"id": 0}),
            USER_ID: 0,
            UUID_FIELD: "",
            IP_ADDRESS: "",
            DEVICE_NAME: "",
        }

    @property
    def access_token_claims(self):
        return {
            **self._setting("ACCESS_TOKEN_CLAIMS", {"id": 0}),
            USER_ID: 0,
            UUID_FIELD: "",
            IP_ADDRESS: "",
            DEVICE_NAME: "",
        }

    @property
    def access_token_user_field_claims(self):
        return {
            **self._setting("ACCESS_TOKEN_USER_FIELD_CLAIMS", {"id": 0}),
            USER_ID: 0,
        }

    @property
    def encrypt_key(self):
        return self._setting("ENCRYPT_KEY", self.encryption_key)

    @property
    def cache_using(self):
        return self._setting("CACHE_USING", False)

    @property
    def get_user_by_access_token(self):
        return self._setting("GET_USER_BY_ACCESS_TOKEN", False)

    @property
    def get_device_limit(self):
        return self._setting("DEVICE_LIMIT", None)


@functools.lru_cache
def jwt_auth_app_settings() -> AppSettings:
    return AppSettings("JWT_AUTH_", get_random_bytes(32))


app_setting = jwt_auth_app_settings()
