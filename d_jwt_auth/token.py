from typing import Dict

from django.http import HttpRequest
from rest_framework_simplejwt.tokens import Token, UntypedToken
from rest_framework_simplejwt.tokens import TokenError as BaseTokenError
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from .app_settings import app_setting
from .constants import ACCESS_TOKEN, REFRESH_TOKEN, UUID_FIELD, USER_ID, TOKEN_TYPE, DEVICE_NAME, IP_ADDRESS
from .encryption import encrypt, decrypt
from .exceptions import TokenError
from .client import get_client_info
from .services import get_user_auth_uuid
from .models import UserAuth

User = get_user_model()


class AccessToken(Token):
    lifetime = app_setting.access_token_lifetime
    token_type = ACCESS_TOKEN


class RefreshToken(Token):
    lifetime = app_setting.refresh_token_lifetime
    token_type = REFRESH_TOKEN


def set_token_claims(*, token: Token, claims: Dict, **kwargs):
    for key in claims:
        claims[key] = kwargs[key]

    for key, value in claims.items():
        token[key] = value


def get_token_claims(*, token: Token, claims: Dict):
    for key in claims:
        claims[key] = token.get(key)


def generate_refresh_token_with_claims(**kwargs) -> str:
    refresh_token = RefreshToken()

    kwargs[UUID_FIELD] = get_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.REFRESH_TOKEN)
    set_token_claims(token=refresh_token, claims=app_setting.refresh_token_claims, **kwargs)

    refresh_token = encrypt_token(refresh_token)

    return refresh_token


def generate_access_token_with_claims(**kwargs) -> str:
    access_token = AccessToken()

    kwargs[UUID_FIELD] = get_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.ACCESS_TOKEN)
    set_token_claims(token=access_token, claims=app_setting.access_token_claims, **kwargs)

    access_token = encrypt_token(access_token)

    return access_token


def get_user_by_access_token(token: Token) -> User:
    claims = app_setting.access_token_user_field_claims

    get_token_claims(token=token, claims=claims)

    return User(
        **claims
    )


def encrypt_token(token: Token) -> str:
    return encrypt(data=str(token), key=app_setting.encrypt_key)


def decrypt_token(token: str) -> str:
    return decrypt(encrypted=token.encode(), key=app_setting.encrypt_key)


def generate_token(request: HttpRequest, user: User) -> Dict:
    client_info = get_client_info(request=request)
    refresh_token = generate_refresh_token_with_claims(**client_info, **user.__dict__)

    access_token = generate_access_token_with_claims(**client_info, **user.__dict__)

    user.last_login = now()
    user.save()

    return {
        ACCESS_TOKEN: access_token,
        REFRESH_TOKEN: refresh_token,
    }


def validate_refresh_token(token: Token, client_info: Dict) -> None:
    if client_info[DEVICE_NAME] != token[DEVICE_NAME]:
        raise TokenError("invalid token")
    uuid_field = get_user_auth_uuid(user_id=token[USER_ID], token_type=UserAuth.REFRESH_TOKEN)
    if uuid_field != token[UUID_FIELD]:
        raise TokenError("invalid uuid")


def validate_access_token(token: Token, client_info: Dict) -> None:
    if client_info[DEVICE_NAME] != token[DEVICE_NAME] or client_info[IP_ADDRESS] != token[IP_ADDRESS]:
        raise TokenError("invalid token")
    uuid_field = get_user_auth_uuid(user_id=token[USER_ID], token_type=UserAuth.ACCESS_TOKEN)
    if uuid_field != token[UUID_FIELD]:
        raise TokenError("invalid token")


def validate_token(request: HttpRequest, raw_token: str) -> Token:
    string_token = decrypt_token(token=raw_token)
    try:
        token = UntypedToken(token=string_token)
    except BaseTokenError as err:
        raise TokenError(err)

    client_info = get_client_info(request=request)

    if token[TOKEN_TYPE] == REFRESH_TOKEN:
        validate_refresh_token(token=token, client_info=client_info)
    elif token[TOKEN_TYPE] == ACCESS_TOKEN:
        validate_access_token(token=token, client_info=client_info)

    return token


def refresh_access_token(request: HttpRequest, raw_refresh_token: str) -> str:
    token = validate_token(request=request, raw_token=raw_refresh_token)

    client_info = get_client_info(request=request)

    validate_refresh_token(token=token, client_info=client_info)

    try:
        user = User.objects.get(id=token["id"])
    except User.DoesNotExist as err:
        raise TokenError(err)

    user.last_login = now()
    user.save()

    return generate_access_token_with_claims(**user.__dict__, **client_info)
