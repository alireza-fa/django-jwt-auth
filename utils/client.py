from typing import Dict

from django.http import HttpRequest

IP_ADDRESS = "ip_address"
DEVICE_NAME = "device_name"


def get_client_info(request: HttpRequest) -> Dict:
    ip_address = request.META.get('REMOTE_ADDR')

    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip_address = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]

    return {
        DEVICE_NAME: request.META.get('HTTP_USER_AGENT', ''),
        IP_ADDRESS: ip_address
    }
