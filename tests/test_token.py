from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import override_settings

from rest_framework.test import APIRequestFactory
from model_bakery import baker

from accounts.models import UserRole
from d_jwt_auth.token import AccessToken, RefreshToken, set_token_claims, get_token_claims, generate_refresh_token_with_claims, \
    generate_access_token_with_claims, encrypt_token, decrypt_token, validate_refresh_token, validate_access_token, \
    validate_token, get_user_by_access_token, generate_token, refresh_access_token, get_token_claims_info
from d_jwt_auth.constants import ACCESS_TOKEN, REFRESH_TOKEN, USER_ID, IP_ADDRESS, DEVICE_NAME, UUID_FIELD
from d_jwt_auth.app_settings import app_setting
from d_jwt_auth.services import get_user_auth_uuid, update_user_auth_uuid
from d_jwt_auth.models import UserAuth
from d_jwt_auth.exceptions import TokenError

User = get_user_model()


class TestToken(TestCase):
    def setUp(self):
        self.ip_address = "127.0.0.1"
        self.device_name = "test-device"
        self.client_info = {IP_ADDRESS: self.ip_address, DEVICE_NAME: self.device_name}
        self.user = baker.make(User)
        self.user_id = self.user.id

    def test_access_token_class(self):
        access_token = AccessToken()
        self.assertEqual(access_token["token_type"], ACCESS_TOKEN)

    def test_refresh_token_class(self):
        refresh_token = RefreshToken()
        self.assertEqual(refresh_token["token_type"], REFRESH_TOKEN)

    def test_set_token_claims(self):
        token = AccessToken()

        claims = {"id": 0, "username": ""}

        set_token_claims(token=token, claims=claims, username="alireza", id=1, email="alireza@gmail.com")

        self.assertEqual(token["username"], "alireza")
        self.assertEqual(token["id"], 1)
        self.assertEqual(token.get("email"), None)

    def test_get_token_claims(self):
        token = RefreshToken()
        token["username"] = "alireza"
        token["id"] = 1

        claims = {"id": 0, "username": "", "email": ""}
        get_token_claims(token=token, claims=claims)

        self.assertEqual(claims["id"], 1)
        self.assertEqual(claims["username"], "alireza")
        self.assertEqual(claims["email"], None)

    def test_encrypt_and_decrypted_token(self):
        token = AccessToken()
        encrypted_token = encrypt_token(token=token)
        decrypted_token = decrypt_token(token=encrypted_token)
        self.assertEqual(str(token), decrypted_token)

    def test_validate_refresh_token_valid_data(self):
        token = RefreshToken()
        claims = app_setting.refresh_token_claims
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.REFRESH_TOKEN)
        set_token_claims(
            token=token,
            claims=claims,
            **{**self.user.__dict__, UUID_FIELD: uuid_field, **self.client_info},
        )
        self.assertIsNone(validate_refresh_token(
            token=token, client_info=self.client_info))

    def test_validate_refresh_token_invalid_uuid(self):
        token = RefreshToken()
        claims = app_setting.refresh_token_claims
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.REFRESH_TOKEN)
        set_token_claims(
            token=token,
            claims=claims,
            **{**self.user.__dict__, UUID_FIELD: uuid_field, **self.client_info},
        )
        update_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.REFRESH_TOKEN)
        with self.assertRaises(TokenError):
            validate_refresh_token(token=token, client_info=self.client_info)

    def test_validate_refresh_token_invalid_device_name(self):
        token = RefreshToken()
        claims = app_setting.refresh_token_claims
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.REFRESH_TOKEN)
        set_token_claims(
            token=token,
            claims=claims,
            **{**self.user.__dict__, UUID_FIELD: uuid_field, **self.client_info},
        )
        with self.assertRaises(TokenError):
            validate_refresh_token(
                token=token,
                client_info={IP_ADDRESS: self.ip_address, DEVICE_NAME: "hacker-device-name"})

    def test_validate_access_token_valid_data(self):
        token = AccessToken()
        claims = app_setting.access_token_claims
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.ACCESS_TOKEN)
        set_token_claims(
            token=token,
            claims=claims,
            **{UUID_FIELD: uuid_field, **self.user.__dict__, **self.client_info},
        )
        self.assertIsNone(validate_access_token(token=token, client_info=self.client_info))

    def test_validate_access_token_invalid_uuid(self):
        token = AccessToken()
        claims = app_setting.access_token_claims
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.ACCESS_TOKEN)
        set_token_claims(
            token=token,
            claims=claims,
            **{**self.user.__dict__, UUID_FIELD: uuid_field, **self.client_info},
        )
        update_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.ACCESS_TOKEN)
        with self.assertRaises(TokenError):
            validate_access_token(token=token, client_info=self.client_info)

    def test_validate_access_token_invalid_device_name(self):
        token = AccessToken()
        claims = app_setting.access_token_claims
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.ACCESS_TOKEN)
        set_token_claims(
            token=token,
            claims=claims,
            **{**self.user.__dict__, UUID_FIELD: uuid_field, **self.client_info},
        )
        with self.assertRaises(TokenError):
            validate_access_token(
                token=token,
                client_info={IP_ADDRESS: self.ip_address, DEVICE_NAME: "hacker-device-name"})

    def test_validate_access_token_invalid_ip_address(self):
        token = AccessToken()
        claims = app_setting.access_token_claims
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.ACCESS_TOKEN)
        set_token_claims(
            token=token,
            claims=claims,
            **{**self.user.__dict__, UUID_FIELD: uuid_field, **self.client_info},
        )
        with self.assertRaises(TokenError):
            validate_access_token(
                token=token,
                client_info={IP_ADDRESS: "127.0.0.2", DEVICE_NAME: self.device_name})

    def test_validate_token(self):
        token = AccessToken()
        claims = app_setting.access_token_claims
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.ACCESS_TOKEN)
        set_token_claims(
            token=token,
            claims=claims,
            **{**self.user.__dict__, UUID_FIELD: uuid_field, **self.client_info},
        )

        encrypted_token = encrypt_token(token=token)
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        token = validate_token(request=request, raw_token=encrypted_token)
        self.assertIsNotNone(token)
        self.assertEqual(token[USER_ID], self.user_id)

    def test_generate_refresh_token_with_claims(self):
        token = generate_refresh_token_with_claims(**{**self.user.__dict__, **self.client_info})
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        token = validate_token(request=request, raw_token=token)
        self.assertEqual(token["token_type"], REFRESH_TOKEN)
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.REFRESH_TOKEN)
        self.assertEqual(uuid_field, token[UUID_FIELD])

    @override_settings(JWT_AUTH_DEVICE_LIMIT=2)
    def test_generate_refresh_token_with_claims_device_limit(self):
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        token1 = generate_refresh_token_with_claims(**{**self.user.__dict__, **self.client_info})
        self.assertIsNotNone(validate_token(request=request, raw_token=token1))
        token2 = generate_refresh_token_with_claims(**{**self.user.__dict__, **self.client_info})
        self.assertIsNotNone(validate_token(request=request, raw_token=token2))
        token3 = generate_refresh_token_with_claims(**{**self.user.__dict__, **self.client_info})
        self.assertIsNotNone(validate_token(request=request, raw_token=token3))
        with self.assertRaises(TokenError):
            validate_token(request=request, raw_token=token1)
        with self.assertRaises(TokenError):
            validate_token(request=request, raw_token=token2)

    @override_settings(JWT_AUTH_DEVICE_LIMIT=2)
    def test_generate_access_token_with_claims_device_limit(self):
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        token1 = generate_access_token_with_claims(**{**self.user.__dict__, **self.client_info})
        self.assertIsNotNone(validate_token(request=request, raw_token=token1))
        token2 = generate_access_token_with_claims(**{**self.user.__dict__, **self.client_info})
        self.assertIsNotNone(validate_token(request=request, raw_token=token2))
        token3 = generate_access_token_with_claims(**{**self.user.__dict__, **self.client_info})
        self.assertIsNotNone(validate_token(request=request, raw_token=token3))
        with self.assertRaises(TokenError):
            validate_token(request=request, raw_token=token1)
        with self.assertRaises(TokenError):
            validate_token(request=request, raw_token=token2)

    def test_generate_access_token_with_claims(self):
        token = generate_access_token_with_claims(**{**self.user.__dict__, **self.client_info})
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        token = validate_token(request=request, raw_token=token)
        self.assertEqual(token["token_type"], ACCESS_TOKEN)
        uuid_field = get_user_auth_uuid(user_id=self.user_id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertEqual(uuid_field, token[UUID_FIELD])

    def test_get_user_by_access_token(self):
        encrypted_token = generate_access_token_with_claims(**{**self.user.__dict__, **self.client_info})
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        token = validate_token(request=request, raw_token=encrypted_token)
        user = get_user_by_access_token(token=token)
        self.assertEqual(user.id, self.user_id)

    def test_generate_token(self):
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        last_login = self.user.last_login
        token = generate_token(request=request, user=self.user)
        user = User.objects.get(id=self.user.id)
        self.assertNotEqual(user.last_login, last_login)
        self.assertEqual(len(token), 2)
        self.assertIsNotNone(token.get(ACCESS_TOKEN))
        self.assertIsNotNone(token.get(REFRESH_TOKEN))

    def test_refresh_access_token(self):
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        refresh_token = generate_refresh_token_with_claims(**self.user.__dict__, **self.client_info)

        last_login = self.user.last_login

        access_token = refresh_access_token(request=request, raw_refresh_token=refresh_token)
        token = validate_token(request=request, raw_token=access_token)
        self.assertEqual(token["token_type"], ACCESS_TOKEN)
        self.assertEqual(token[USER_ID], self.user.id)

        user = User.objects.get(id=self.user.id)
        self.assertNotEqual(user.last_login, last_login)

    def test_refresh_access_token_user_not_exist(self):
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        refresh_token = generate_refresh_token_with_claims(**self.user.__dict__, **self.client_info)

        self.user.delete()

        with self.assertRaises(TokenError):
            refresh_access_token(request=request, raw_refresh_token=refresh_token)

    def test_generate_token_with_roles(self):
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        self.user.roles.create(role=UserRole.DEFAULT)
        self.user.roles.create(role=UserRole.DOCTOR)
        token = generate_token(request=request, user=self.user, roles=list(self.user.roles.all().values_list("role", flat=True)))
        access_token = get_token_claims_info(request=request, raw_token=token["access_token"])
        self.assertEqual(list, type(access_token["roles"]))
        self.assertEqual(len(access_token["roles"]), 2)

    def test_generate_token_with_empty_roles(self):
        request = APIRequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = self.ip_address
        request.META["HTTP_USER_AGENT"] = self.device_name
        token = generate_token(request=request, user=self.user, roles=list(self.user.roles.all().values_list('role', flat=True)))
        access_token = get_token_claims_info(request=request, raw_token=token["access_token"])
        self.assertEqual(access_token["roles"], [])
        self.assertEqual(len(access_token["roles"]), 0)
