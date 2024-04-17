import functools
from datetime import timedelta


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


@functools.lru_cache
def jwt_auth_app_settings() -> AppSettings:
    return AppSettings("JWT_AUTH_")


app_setting = jwt_auth_app_settings()
