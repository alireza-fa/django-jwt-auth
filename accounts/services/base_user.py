from django.contrib.auth import get_user_model

User = get_user_model()


def create_base_user(username: str, phone_number: str, password: str, email: str | None = None) -> User:
    user = User.objects.create_user(username=username, phone_number=phone_number, password=password, email=email)
    return user
