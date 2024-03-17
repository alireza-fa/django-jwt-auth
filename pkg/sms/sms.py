from pkg.sms.dummy.dummy import get_dummy_sms_service


def get_sms_service():
    service_name = "dummy"

    match service_name:
        case "dummy":
            return get_dummy_sms_service()
