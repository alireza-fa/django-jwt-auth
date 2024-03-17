import functools

from pkg.sms.base import Sms


class DummySmsService(Sms):

    def send(self, message: str) -> None:
        print(f"sms sent: {message}")


@functools.cache
def get_dummy_sms_service():
    return DummySmsService()
