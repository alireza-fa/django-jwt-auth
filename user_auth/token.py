from typing import Dict, ByteString

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, Token, UntypedToken

from .models import UserLogin
from .encryption import encrypt, decrypt


User = get_user_model()


def set_token_claims(token: Token, data: Dict) -> Token:
    for key, value in data.items():
        token[key] = value

    return token


def get_token_by_user(user: User, client_info: Dict) -> Dict:
    token = RefreshToken.for_user(user=user)

    token = set_token_claims(token=token, data=client_info)

    return {
        "refresh_token": encrypt(data=str(token)),
        "access_token": encrypt(data=str(token.access_token)),
    }


def check_token_expire(token: Token) -> None:
    if token['exp'] <= timezone.now().timestamp():
        raise ValueError('Invalid token')


def check_validate_refresh_token(refresh_token: str) -> bool:
    try:
        user_login = UserLogin.objects.get(refresh_token=encrypt(data=str(refresh_token)))
    except UserLogin.DoesNotExist:
        raise ValueError('Invalid token.')
    return user_login


def check_token_device(token: Token, client_info: Dict) -> None:
    """
    :return: if token is valid, return Token else raise Exception
    """
    if token['device_name'] != client_info['device_name']:
        raise ValueError('Invalid token.')


def validated_token(encrypted_token: ByteString, client_info: Dict) -> Token:
    decrypted_token = decrypt(encrypted=encrypted_token)

    try:
        token = UntypedToken(token=decrypted_token)
    except TokenError:
        raise ValueError('Invalid token.')

    check_token_device(token=token, client_info=client_info)

    if token['token_type'] == 'refresh':
        check_validate_refresh_token(refresh_token=str(token))

    return token


def validate_refresh_token(refresh_token: str, client_info: Dict) -> Token:
    try:
        token = RefreshToken(token=refresh_token)
    except TokenError:
        raise ValueError('Invalid token')

    check_token_expire(token=token)

    check_token_device(token=token, client_info=client_info)

    return token


def get_new_access_token(encrypted_refresh_token: ByteString, client_info: Dict) -> str:
    decrypted_refresh_token = decrypt(encrypted=encrypted_refresh_token)

    token = validate_refresh_token(refresh_token=decrypted_refresh_token, client_info=client_info)

    check_validate_refresh_token(refresh_token=str(token))

    encrypted_access_token = encrypt(data=str(token.access_token))

    return encrypted_access_token


def verify_token(token: Token, client_info: Dict) -> bool:
    if token['device_name'] != client_info['device_name'] or token['ip_address'] != client_info['ip_address']:
        return False
    return True


def black_refresh_token(encrypted_refresh_token: ByteString, client_info: Dict) -> None:
    decrypted_token = decrypt(encrypted=encrypted_refresh_token)

    token = validate_refresh_token(refresh_token=decrypted_token, client_info=client_info)

    try:
        user_login = UserLogin.objects.get(refresh_token=encrypt(data=str(token)))
    except UserLogin.DoesNotExist:
        raise ValueError('Invalid token')

    user_login.delete()
