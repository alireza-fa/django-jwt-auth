import re

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from utils.converter import persian_to_english

email_regex = r'^([a-z0-9]+[.-_]*)*[a-z0-9]+@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-zA-Z]{2,}$'


def validate_email(email: str) -> bool:
    if re.search(email_regex, email):
        return True
    else:
        return False


def validate_phone_number(phone_number) -> object or None:
    number = persian_to_english(phone_number)

    if len(number) != 11 or not number.startswith('09'):
        raise ValidationError(_('Invalid phone number'))

    return number
