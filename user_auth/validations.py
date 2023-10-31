from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _


_english_to_persian = {
    "0": '۰',
    "1": '۱',
    "2": '۲',
    "3": '۳',
    "4": '۴',
    "5": '۵',
    "6": '۶',
    "7": '۷',
    "8": '۸',
    "9": '۹'
}

_persian_to_english = {
    "۰": '0',
    "۱": '1',
    "۲": '2',
    "۳": '3',
    "۴": '4',
    "۵": '5',
    "۶": '6',
    "۷": '7',
    "۸": '8',
    "۹": '9'
}


def persian_to_english(number: str) -> str:
    number = str(number)
    num = str()

    for i in number:
        item = _persian_to_english.get(i)
        if item:
            num += item
        else:
            item = _english_to_persian.get(i)
            if item:
                num += i
    return num


def validate_phone_number(phone_number) -> object or None:
    number = persian_to_english(phone_number)

    if len(number) != 11 or not number.startswith('09'):
        raise ValidationError(_('Invalid phone number'))

    return number
