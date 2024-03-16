from typing import Dict

from django.contrib.auth import get_user_model
from django.http import HttpRequest

from pkg.token.token import generate_refresh_token_with_claims, generate_access_token_with_claims
from utils import client
from authentication.services.token import encrypt_token, get_refresh_token_claims, get_access_token_claims

User = get_user_model()


def login_by_password(request: HttpRequest, username: str, password: str) -> Dict:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist as err:
        raise ValueError(err)

    if not user.check_password(password):
        raise ValueError("user does not exist")

    client_info = client.get_client_info(request=request)

    refresh_token = generate_refresh_token_with_claims(
        claims=get_refresh_token_claims(**client_info, user_id=user.id), encrypt_func=encrypt_token)

    access_token = generate_access_token_with_claims(
        claims=get_access_token_claims(**client_info, **user.__dict__),
        encrypt_func=encrypt_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def register_user(request: HttpRequest, username: str, email: str, password: str) -> Dict:
    user = User.objects.create_user(username=username, email=email, password=password)

    client_info = client.get_client_info(request=request)

    refresh_token = generate_refresh_token_with_claims(
        claims=get_refresh_token_claims(**client_info, user_id=user.id), encrypt_func=encrypt_token)

    access_token = generate_access_token_with_claims(
        claims=get_access_token_claims(**client_info, **user.__dict__),
        encrypt_func=encrypt_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
