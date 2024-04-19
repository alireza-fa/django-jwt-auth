from datetime import timedelta

from django.test import SimpleTestCase, override_settings

from d_jwt_auth.app_settings import app_setting
from d_jwt_auth.constants import USER_ID, UUID_FIELD, IP_ADDRESS, DEVICE_NAME


class TestAppSettngs(SimpleTestCase):

    def test_access_token_lifetime_default(self):
        lifetime = app_setting.access_token_lifetime
        self.assertIsNotNone(lifetime)
        self.assertEqual(type(lifetime), timedelta)

    @override_settings(JWT_AUTH_ACCESS_TOKEN_LIFETIME=timedelta(minutes=5))
    def test_access_token_lifetime(self):
        lifetime = app_setting.access_token_lifetime
        self.assertLess(lifetime, timedelta(minutes=10))

    @override_settings(JWT_AUTH_REFRESH_TOKEN_LIFETIME=timedelta(days=15))
    def test_refresh_lifetime(self):
        lifetime = app_setting.refresh_token_lifetime
        self.assertLess(lifetime, timedelta(days=30))

    def test_refresh_token_claim_default(self):
        claims = app_setting.refresh_token_claims
        self.assertEqual(claims, {
            USER_ID: 0,
            UUID_FIELD: "",
            IP_ADDRESS: "",
            DEVICE_NAME: "",
        })

    @override_settings(JWT_AUTH_REFRESH_TOKEN_CLAIMS={
        "username": "",
        "email": "",
    })
    def test_refresh_token_claims(self):
        claims = app_setting.refresh_token_claims
        self.assertEqual(claims, {
            USER_ID: 0,
            UUID_FIELD: "",
            IP_ADDRESS: "",
            DEVICE_NAME: "",
            "username": "",
            "email": "",
        })

    def test_access_token_claim_default(self):
        claims = app_setting.refresh_token_claims
        self.assertEqual(claims, {
            USER_ID: 0,
            UUID_FIELD: "",
            IP_ADDRESS: "",
            DEVICE_NAME: "",
        })

    @override_settings(JWT_AUTH_REFRESH_TOKEN_CLAIMS={
        "username": "",
        "email": "",
        "fullname": "",
    })
    def test_refresh_token_claims(self):
        claims = app_setting.refresh_token_claims
        self.assertEqual(claims, {
            USER_ID: 0,
            UUID_FIELD: "",
            IP_ADDRESS: "",
            DEVICE_NAME: "",
            "username": "",
            "email": "",
            "fullname": "",
        })

    @override_settings(JWT_AUTH_ACCESS_TOKEN_USER_FIELD_CLAIMS={
        USER_ID: 0,
        "username": "",
        "email": "",
    })
    def test_access_token_user_field(self):
        user_fields = app_setting.access_token_user_field_claims
        self.assertEqual(user_fields, {
            USER_ID: 0,
            "username": "",
            "email": "",
        })
