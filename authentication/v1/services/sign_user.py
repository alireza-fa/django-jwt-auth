from typing import Dict

from django.contrib.auth import get_user_model
from django.http import HttpRequest

from accounts.selectors.base_user import get_user_by_phone_number, get_user_by_username
from utils.otp import generate_otp_code
from authentication.exceptions import IpBlocked, AuthFieldNotAllowedToReceiveSms, InvalidCode
from pkg.sms.sms import get_sms_service
from utils import client
from authentication.v1.services.token import generate_token
from utils.cache import get_cache, set_cache, incr_cache, delete_cache

User = get_user_model()
SIGN_SUF_KEY = "sign"


def login_by_password(request: HttpRequest, username: str, password: str) -> Dict:
    user = get_user_by_username(username=username)

    if not user.check_password(password):
        raise ValueError("user does not exist")

    client_info = client.get_client_info(request=request)

    return generate_token(client_info=client_info, user=user)


def check_ip_address_access(ip_address: str) -> bool:
    key = ip_address + "count"
    count = get_cache(key=key)
    if not count:
        set_cache(key=key, value=1, timeout=86400)
        return True

    if count <= 10:
        incr_cache(key=key)
        return True

    return False


def check_auth_field_allow_to_receive_sms(auth_field, client_info):
    if get_cache(key=auth_field+SIGN_SUF_KEY):
        raise AuthFieldNotAllowedToReceiveSms


def login_by_phone_number(request: HttpRequest, phone_number: str) -> None:
    client_info = client.get_client_info(request=request)

    check_auth_field_allow_to_receive_sms(auth_field=phone_number, client_info=client_info)

    if not check_ip_address_access(ip_address=client_info[client.IP_ADDRESS]):
        raise IpBlocked

    get_user_by_phone_number(phone_number=phone_number)

    code = generate_otp_code()

    set_cache(key=phone_number+SIGN_SUF_KEY, value={"code": code, "phone_number": phone_number, "state": "login"},
              timeout=120)

    sms = get_sms_service()
    sms.send(code)


def check_validate_auth_field_for_verify(auth_field: str, client_info: Dict):
    key = auth_field + "count"
    count = get_cache(key=key)

    if not count:
        set_cache(key=key, value=1, timeout=120)
        count = 1

    if count <= 5:
        incr_cache(key=key)
        return None

    raise InvalidCode


def login_state(client_info: Dict, phone_number: str) -> Dict:
    user = get_user_by_phone_number(phone_number=phone_number)

    return generate_token(client_info=client_info, user=user)


def register_state(client_info: Dict, username: str, phone_number: str, password: str, email: str | None = None) -> Dict:
    user = User.objects.create_user(username=username, phone_number=phone_number, password=password)

    return generate_token(client_info=client_info, user=user)


def verify_sign_user(request: HttpRequest, phone_number: str, code: str) -> Dict:
    client_info = client.get_client_info(request=request)
    check_validate_auth_field_for_verify(auth_field=phone_number, client_info=client_info)

    cache_info = get_cache(key=phone_number+SIGN_SUF_KEY)
    if not cache_info:
        raise InvalidCode

    if cache_info["code"] != code:
        raise InvalidCode

    if cache_info["state"] == "login":
        delete_cache(key=phone_number+SIGN_SUF_KEY)
        return login_state(client_info=client_info, phone_number=phone_number)

    delete_cache(key=phone_number+SIGN_SUF_KEY)
    return register_state(client_info=client_info, username=cache_info["username"],
                          phone_number=cache_info["phone_number"], password=cache_info["password"],
                          email=cache_info["email"])


def register_user(request: HttpRequest, username: str, phone_number: str, password: str, email: str | None = None) -> None:
    client_info = client.get_client_info(request=request)
    check_auth_field_allow_to_receive_sms(auth_field=phone_number, client_info=client_info)

    if not check_ip_address_access(ip_address=client_info[client.IP_ADDRESS]):
        raise IpBlocked

    code = generate_otp_code()

    set_cache(
        key=phone_number+SIGN_SUF_KEY,
        value={"code": code, "phone_number": phone_number, "username": username,
               "password": password, "email": email, "state": "register"}, timeout=120)

    sms = get_sms_service()
    sms.send(code)
