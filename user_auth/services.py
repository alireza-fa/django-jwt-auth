from datetime import datetime
from typing import Dict, Optional
from random import randint

from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone

from .models import UserLogin
from .cache import (set_user_login_cache, set_user_register_cache, delete_user_auth_cache,
                    get_cache, incr_cache, set_cache)

User = get_user_model()


def set_refresh_expired_at() -> datetime:
    return timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']


def get_client_info(request: object) -> Dict:
    return {
        "device_name": request.META.get('HTTP_USER_AGENT', ''),
        "ip_address": request.META.get('REMOTE_ADDR'),
    }


def generate_otp_code() -> str:
    return str(randint(a=100000, b=999999))


def get_user_login_by_refresh_token(refresh_token) -> UserLogin:
    return UserLogin.objects.get(refresh_token=refresh_token)


def create_user_login(user: User, token: Dict, client_info: Dict) -> UserLogin:
    devices = UserLogin.objects.filter(user=user)
    if devices.count() >= 2:
        devices.last().delete()

    return UserLogin.objects.create(
        user=user,
        refresh_token=token['refresh'],
        device_name=client_info['device_name'],
        ip_address=client_info['ip_address'],
        last_login=timezone.now(),
        expired_at=set_refresh_expired_at(),
    )


def check_number_allow_to_receive_sms(phone_number: str) -> bool:
    """
     Each number can only receive up to ten SMS for the code every twenty-four hours
    """
    key = phone_number + 'otp_sms_count'

    sms_receive_count = get_cache(key=key)

    if sms_receive_count:
        if sms_receive_count >= 5:
            return False
    else:
        set_cache(key=key, value=1, timeout=86400)
        return True

    incr_cache(key=key)

    return True


def user_login_func(request: HttpRequest, phone_number: str) -> None:
    allow_sms = check_number_allow_to_receive_sms(phone_number=phone_number)
    if allow_sms is False:
        raise PermissionError('access denied.')

    code = generate_otp_code()

    client_info = get_client_info(request=request)

    set_user_login_cache(client_info=client_info, code=code, phone_number=phone_number)

    # TODO: send sms


def user_register_func(request: HttpRequest, phone_number: str, fullname: str,
                       email: Optional[str] = None) -> None:
    allow_sms = check_number_allow_to_receive_sms(phone_number=phone_number)
    if allow_sms is False:
        raise PermissionError('access denied.')

    code = generate_otp_code()

    client_info = get_client_info(request=request)

    set_user_register_cache(
        client_info=client_info, code=code, phone_number=phone_number,
        fullname=fullname, email=email)

    # TODO: send sms


def user_verify_func():
    pass


def user_resend_func():
    pass


def user_refresh_func():
    pass


def user_logout_func():
    pass
