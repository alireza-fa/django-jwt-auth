# Auth
PHONE_NUMBER_DESCRIPTION = "just iranian phone number like example value(not +98 or 0098)"
LOGIN_BY_PHONE_NUMBER_EXAMPLE_VALUE = {"phone_number": "09129121111"}
LOGIN_BY_PHONE_NUMBER_200_DESCRIPTION = ("If the mobile number entered is correct. A code will be sent to the user"
                                         " phone number.")
IP_BLOCKED_DESCRIPTION = "If an IP address tries too many times to login. will be blocked"

VERIFY_SIGN_EXAMPLE_VALUE = {"phone_number": "09129121111", "code": "123456"}
OTP_CODE_DESCRIPTION = "The code must be six numeric characters. Its format is string"

REGISTER_EXAMPLE_VALUE = {"username": "alireza", "phone_number": "09129121111", "password": "password"}
USERNAME_DESCRIPTION = "Required and unique. 32 characters or fewer. Letters, digits and @/./+/-/_ only."
REGISTER_200_DESCRIPTION = "If registration successfully. A code will be sent to the user phone number."

# Padlock
PADLOCK_THUMBNAIL_DESCRIPTION = "The cover should be a photo and its size should be less than 1 MB"
PADLOCK_FILE_DESCRIPTION = "The file can be in any format, but its size must be less than 100 MB"
PADLOCK_REVIEW_DESCRIPTION = ("If you want your file to be reviewed by support and its correctness confirmed,"
                              " set this field equal to true. otherwise equal to false")
PADLOCK_PRICE_DESCRIPTION = "The price is in numbers and its currency is Tomans"
PADLOCK_CREATE_EXAMPLE_VALUE = {
    "title": "a private padlock",
    "description": "It is a private padlock and will be unlocked for you when you pay for it.",
    "thumbnail": "uploading image here",
    "file": "uploading your file here",
    "review_active": True,
    "price": 23000,
}

# Accounts
BASE_USER_UPDATE_EXAMPLE_VALUE = {"username": "alireza"}
