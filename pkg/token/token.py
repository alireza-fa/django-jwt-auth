from typing import Dict

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, Token, UntypedToken, TokenError


def set_token_claims(*, token: Token, claims: Dict):
    for key, value in claims.items():
        token[key] = value


def get_token_claims(*, token: Token, claims: Dict):
    for key in claims:
        claims[key] = token[key]


def get_token_string_claims(*, string_token: str, claims: Dict):
    token = validate_token(string_token=string_token)

    for key in claims:
        claims[key] = token[key]


def encrypt_token_function(token: Token) -> str:
    pass


def generate_refresh_token_with_claims(*, claims: Dict, encrypt_func: encrypt_token_function or None = None) -> Token:
    refresh_token = RefreshToken()

    set_token_claims(token=refresh_token, claims=claims)

    if encrypt_func:
        refresh_token = encrypt_func(refresh_token)

    return refresh_token


def generate_access_token_with_claims(*, claims: Dict, encrypt_func: encrypt_token_function or None = None):
    access_token = AccessToken()

    set_token_claims(token=access_token, claims=claims)

    if encrypt_func:
        access_token = encrypt_func(access_token)

    return access_token


def validate_token_function(token: Token):
    pass


def validate_token(string_token: str, func: validate_token_function or None = None) -> Token:
    try:
        token = UntypedToken(token=string_token)
    except TokenError as err:
        raise ValueError(err)

    if func:
        func(token=token)

    return token
