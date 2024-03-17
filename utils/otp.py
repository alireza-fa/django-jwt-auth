from random import randint


def generate_otp_code() -> str:
    return str(randint(a=100000, b=999999))
