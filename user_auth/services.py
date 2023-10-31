from datetime import datetime
from typing import Dict, Optional
from random import randint

from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone

from .models import UserLogin
from .cache import (set_user_login_cache, set_user_register_cache, delete_user_auth_cache,
                    get_cache, incr_cache, set_cache, set_user_resend_cache,)
from .token import get_token_by_user
from accounts.serializers import UserProfileSerializer


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
        refresh_token=token['refresh_token'],
        device_name=client_info['device_name'],
        ip_address=client_info['ip_address'],
        last_login=timezone.now(),
        expired_at=set_refresh_expired_at(),
    )


# ========================== User Login And Register ===========================
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
# ============ End User Login And Register ===========================================


# ============ User Verify =====================================================
def check_access_to_try(phone_number: str) -> None:
    key_try = phone_number + 'try'

    try_count = get_cache(key=key_try)

    if try_count is None:
        raise ValueError('Invalid code.')

    if try_count >= 5:
        raise ValueError('Invalid code.')

    incr_cache(key=key_try)


def validate_code(phone_number: str, code: str, client_info) -> Dict:
    check_access_to_try(phone_number=phone_number)

    cache_info = get_cache(key=phone_number)

    if cache_info is None:
        raise ValueError('Invalid code.')

    if cache_info['code'] != code:
        raise ValueError('Invalid code.')

    if cache_info['client_info'] != client_info:
        raise ValueError('Invalid code')

    return cache_info


def user_verify_func(request: HttpRequest, code: str, phone_number: str) -> Dict:
    client_info = get_client_info(request=request)

    cache_info = validate_code(phone_number=phone_number, code=code, client_info=client_info)

    if cache_info['state'] == 'register':
        user = User.objects.create_user(phone_number=phone_number, fullname=cache_info['fullname'],
                                        email=cache_info['email'])
    else:
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise ValueError('Invalid code.')

    delete_user_auth_cache(phone_number=phone_number)

    token = get_token_by_user(user=user, client_info=client_info)

    create_user_login(user=user, token=token, client_info=client_info)

    serializer = UserProfileSerializer(instance=user)

    data = {"user": serializer.data, "token": token}

    return data
# ============= End User Verify ==================================


def user_resend_func(phone_number: str, request: HttpRequest) -> None:
    user_info = get_cache(key=phone_number + 'info')

    if user_info is None:
        raise PermissionError('access denied.')

    allow_sms = check_number_allow_to_receive_sms(phone_number=phone_number)
    if allow_sms is False:
        raise PermissionError('access denied.')

    code = generate_otp_code()

    client_info = get_client_info(request=request)

    if client_info != user_info['client_info']:
        raise PermissionError('access denied.')

    set_user_resend_cache(code=code, **user_info)

    # TODO: send sms


def user_refresh_func():
    pass


def user_logout_func():
    pass
