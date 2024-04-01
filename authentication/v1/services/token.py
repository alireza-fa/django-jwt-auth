from typing import Dict

from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework_simplejwt.tokens import Token

from pkg.encrypto.encryption import encrypt, decrypt
from utils import client
from pkg.token.token import (generate_access_token_with_claims, get_token_claims,
                             generate_refresh_token_with_claims, validate_token)
from utils.cache import set_cache, get_cache

User = get_user_model()

IP_ADDRESS = "ip_address"
DEVICE_NAME = "device_name"
USER_ID = "id"
USERNAME = "username"
EMAIL = "email"
IS_ACTIVE = "is_active"
IS_ADMIN = "is_admin"

refresh_token_claims = {
    IP_ADDRESS: "",
    DEVICE_NAME: "",
    USER_ID: 0,
}

access_token_claims = {
    IP_ADDRESS: "",
    DEVICE_NAME: "",
    USER_ID: 0,
    USERNAME: "",
    EMAIL: "",
    IS_ACTIVE: False,
    IS_ADMIN: False,
}

user_to_map = {
    USER_ID: 0,
    USERNAME: "",
    EMAIL: "",
    IS_ACTIVE: "",
    IS_ADMIN: "",
}


def get_refresh_token_claims(**kwargs) -> Dict:
    claims = refresh_token_claims
    claims[IP_ADDRESS] = ""
    claims[DEVICE_NAME] = ""

    for key in claims:
        claims[key] = kwargs[key]

    return claims


def get_access_token_claims(**kwargs) -> Dict:
    claims = access_token_claims
    claims[IP_ADDRESS] = ""
    claims[DEVICE_NAME] = ""

    for key in claims:
        claims[key] = kwargs[key]

    return claims


def encrypt_token(token: Token) -> str:
    return encrypt(data=str(token), key=settings.ENCRYPT_KEY)


def decrypt_token(token: str) -> str:
    return decrypt(encrypted=token.encode(), key=settings.ENCRYPT_KEY)


def verify_token_func(token: Token):
    if token["token_type"] == "refresh":
        if get_cache(key=str(token)):
            raise ValueError("Invalid refresh token")


def verify_token(*, request: HttpRequest, token: str) -> bool:
    try:
        token_string = decrypt_token(token=token)
        token = validate_token(string_token=token_string, func=verify_token_func)
    except ValueError:
        return False

    client_info = client.get_client_info(request=request)
    if token[DEVICE_NAME] != client_info[client.DEVICE_NAME]:
        return False

    return True


def validate_refresh_token(token: Token):
    if token["token_type"] != "refresh":
        raise ValueError("Invalid refresh token")
    if get_cache(key=str(token)):
        raise ValueError("Invalid refresh token")


def refresh_access_token(request: HttpRequest, refresh_token: str) -> str:
    refresh_token_str = decrypt_token(token=refresh_token)

    token = validate_token(string_token=refresh_token_str, func=validate_refresh_token)

    user = User.objects.get(id=token[USER_ID])

    client_info = client.get_client_info(request=request)
    claims = get_access_token_claims(**client_info, **user.__dict__)

    user.last_login = timezone.now()
    user.save()

    return generate_access_token_with_claims(claims=claims, encrypt_func=encrypt_token)


def get_user_by_access_token(token: Token) -> User:
    claims = user_to_map
    get_token_claims(token=token, claims=claims)

    return User(
        **user_to_map
    )


def generate_token(client_info: Dict, user: User) -> Dict:
    refresh_token = generate_refresh_token_with_claims(
        claims=get_refresh_token_claims(**client_info, id=user.id), encrypt_func=encrypt_token)

    access_token = generate_access_token_with_claims(
        claims=get_access_token_claims(**client_info, **user.__dict__),
        encrypt_func=encrypt_token)

    user.last_login = timezone.now()
    user.save()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def ban_token(encrypted_token: str) -> None:
    decrypted_token = decrypt_token(token=encrypted_token)

    token = validate_token(string_token=decrypted_token, func=validate_refresh_token)

    set_cache(key=str(token), value=1, timeout=settings.REFRESH_TOKEN_TOKEN_LIFETIME_TO_DAYS*24*60*60)
