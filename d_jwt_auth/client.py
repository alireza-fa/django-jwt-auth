import ipaddress
from typing import Dict

from django.http import HttpRequest

IP_ADDRESS = "ip_address"
DEVICE_NAME = "device_name"


def get_ip_address(request: HttpRequest) -> str:
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip_address:
        ip_address = ip_address.split(",")[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR", '').split(",")[0]

    possibles = (ip_address.lstrip("[").split("]")[0], ip_address.split(":")[0])

    for addr in possibles:
        try:
            return str(ipaddress.ip_address(addr))
        except:
            pass

    return ip_address


def get_client_info(request: HttpRequest) -> Dict:
    return {
        DEVICE_NAME: request.META.get('HTTP_USER_AGENT', ''),
        IP_ADDRESS: get_ip_address(request=request)
    }
