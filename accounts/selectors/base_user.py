from django.contrib.auth import get_user_model


User = get_user_model()


def get_user_by_phone_number(phone_number: str) -> User:
    return User.objects.get(phone_number=phone_number)


def get_user_by_username(username: str) -> User:
    return User.objects.get(username=username)
