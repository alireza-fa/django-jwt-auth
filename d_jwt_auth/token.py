from typing import Dict

from django.http import HttpRequest
from rest_framework_simplejwt.tokens import Token, UntypedToken
from rest_framework_simplejwt.tokens import TokenError as BaseTokenError
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from .app_settings import app_setting
from .encrypto.encryption import encrypt, decrypt
from .exceptions import CheckClaimsErr, TokenError
from .client import get_client_info, IP_ADDRESS, DEVICE_NAME

User = get_user_model()


ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"
TOKEN_TYPE = "token_type"


class AccessToken(Token):
    lifetime = app_setting.access_token_lifetime_minutes
    token_type = ACCESS_TOKEN


class RefreshToken(Token):
    lifetime = app_setting.refresh_token_lifetime_days
    token_type = REFRESH_TOKEN


def set_token_claims(*, token: Token, claims: Dict, **kwargs):
    for key in claims:
        claims[key] = kwargs[key]

    for key, value in claims.items():
        token[key] = value


def get_token_claims(*, token: Token, claims: Dict):
    for key in claims:
        claims[key] = token[key]


def get_token_string_claims(*, token: Token, claims: Dict):
    for key in claims:
        claims[key] = token[key]


def generate_refresh_token_with_claims(**kwargs) -> str:
    refresh_token = RefreshToken()

    set_token_claims(token=refresh_token, claims=app_setting.refresh_token_claims, **kwargs)

    refresh_token = encrypt_token(refresh_token)

    return refresh_token


def generate_access_token_with_claims(**kwargs) -> str:
    access_token = AccessToken()

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
    refresh_token = generate_refresh_token_with_claims(encrypt_func=encrypt_token, **client_info, **user.__dict__)

    access_token = generate_access_token_with_claims(encrypt_func=encrypt_token, **client_info, **user.__dict__)

    user.update(last_login=now())

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def validate_refresh_token(token: Token, client_info: Dict) -> None:
    if client_info[DEVICE_NAME] != token[DEVICE_NAME]:
        raise TokenError("invalid token")


def validate_access_token(token: Token, client_info: Dict) -> None:
    if client_info[DEVICE_NAME] != token[DEVICE_NAME] or client_info[IP_ADDRESS] != token[IP_ADDRESS]:
        raise TokenError("invalid token")


def validate_token(request: HttpRequest, string_token: str) -> Token:
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


def refresh_access_token(check_claims: dict, request: HttpRequest, refresh_token: str) -> str:
    refresh_token_str = decrypt_token(token=refresh_token)

    token = validate_token(string_token=refresh_token_str)

    client_info = get_client_info(request=request)
    if token[DEVICE_NAME] != client_info[DEVICE_NAME]:
        raise TokenError

    user = User.objects.get(id=token["id"])

    for key, value in check_claims.items():
        if check_claims[key] == token[key]:
            raise CheckClaimsErr(f"{key} value not match with token value: token: {token[key]} != {value}")

    user.update(last_login=now())

    return generate_access_token_with_claims(encrypt_func=encrypt_token, **user.__dict__)


def ban_token(encrypted_token: str) -> None:
    decrypted_token = decrypt_token(token=encrypted_token)

    # token = validate_token(string_token=decrypted_token, func=validate_refresh_token)
    #
    # set_cache(key=str(token), value=1, timeout=settings.REFRESH_TOKEN_TOKEN_LIFETIME_TO_DAYS*24*60*60)
