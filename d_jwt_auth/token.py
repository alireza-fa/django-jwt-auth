from typing import Dict
from datetime import datetime

from django.http import HttpRequest
from rest_framework_simplejwt.tokens import Token, UntypedToken
from rest_framework_simplejwt.tokens import TokenError as BaseTokenError
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db.models.fields.files import File

from .app_settings import app_setting
from .constants import ACCESS_TOKEN, REFRESH_TOKEN, UUID_FIELD, USER_ID, TOKEN_TYPE, DEVICE_NAME, IP_ADDRESS
from .encryption import encrypt, decrypt
from .exceptions import TokenError
from .client import get_client_info
from .services import get_user_auth_uuid, update_user_auth_uuid, get_user_auth
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
        claims[key] = kwargs.get(key)

    for key, value in claims.items():
        if isinstance(value, File):
            if value:
                token[key] = value.url
            else:
                token[key] = None
        elif isinstance(value, datetime):
            token[key] = str(value)
        else:
            token[key] = value


def get_token_claims(*, token: Token, claims: Dict):
    for key in claims:
        claims[key] = token.get(key)


def generate_refresh_token_with_claims(**kwargs) -> str:
    refresh_token = RefreshToken()

    if app_setting.get_device_limit:
        user_auth = get_user_auth(user_id=kwargs[USER_ID], token_type=UserAuth.REFRESH_TOKEN)
        if user_auth.device_login_count >= app_setting.get_device_limit:
            user_auth.device_login_count = 0
            uuid = update_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.REFRESH_TOKEN)
            kwargs[UUID_FIELD] = uuid
            user_auth.uuid = uuid
        else:
            kwargs[UUID_FIELD] = str(user_auth.uuid)
        user_auth.device_login_count += 1
        user_auth.save()
    else:
        kwargs[UUID_FIELD] = get_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.REFRESH_TOKEN)

    set_token_claims(token=refresh_token, claims=app_setting.refresh_token_claims, **kwargs)

    refresh_token = encrypt_token(refresh_token)

    return refresh_token


def generate_access_token_with_claims(**kwargs) -> str:
    access_token = AccessToken()

    if app_setting.get_device_limit:
        user_auth = get_user_auth(user_id=kwargs[USER_ID], token_type=UserAuth.ACCESS_TOKEN)
        if user_auth.device_login_count >= app_setting.get_device_limit:
            user_auth.device_login_count = 0
            uuid = update_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.ACCESS_TOKEN)
            kwargs[UUID_FIELD] = uuid
            user_auth.uuid = uuid
        else:
            kwargs[UUID_FIELD] = str(user_auth.uuid)
        user_auth.device_login_count += 1
        user_auth.save()
    else:
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
    try:
        encrypted_token = encrypt(data=str(token), key=app_setting.encrypt_key)
    except ValueError as err:
        raise TokenError(err)
    return encrypted_token


def decrypt_token(token: str) -> str:
    try:
        decrypted_token = decrypt(encrypted=token.encode(), key=app_setting.encrypt_key)
    except ValueError as err:
        raise TokenError(err)
    return decrypted_token


def generate_token(request: HttpRequest, user: User, **kwargs) -> Dict:
    client_info = get_client_info(request=request)
    refresh_token = generate_refresh_token_with_claims(**client_info, **user.__dict__, **kwargs)

    access_token = generate_access_token_with_claims(**client_info, **user.__dict__, **kwargs)

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
        user = User.objects.get(id=token[USER_ID])
    except User.DoesNotExist as err:
        raise TokenError(err)

    user.last_login = now()
    user.save()

    return generate_access_token_with_claims(**user.__dict__, **client_info)


def verify_token(request: HttpRequest, raw_token: str) -> bool:
    try:
        validate_token(request=request, raw_token=raw_token)
    except TokenError:
        return False
    return True


def get_token_claims_info(request: HttpRequest, raw_token: str) -> Dict:
    token = validate_token(request=request, raw_token=raw_token)
    if token[TOKEN_TYPE] == REFRESH_TOKEN:
        refresh_claims = app_setting.refresh_token_claims
        get_token_claims(token=token, claims=refresh_claims)
        return refresh_claims
    else:
        access_claims = app_setting.access_token_claims
        get_token_claims(token=token, claims=access_claims)
        return access_claims
