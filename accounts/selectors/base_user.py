from django.contrib.auth import get_user_model

from accounts.exceptions import UserNotFound

User = get_user_model()


def get_user_by_phone_number(phone_number: str) -> User:
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        raise UserNotFound

    return user


def get_user_by_username(username: str) -> User:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise UserNotFound

    return user
