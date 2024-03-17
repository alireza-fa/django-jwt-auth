# 2000
OK = 2000
CREATED = 2010
# 4000
NOT_ACCEPTABLE = 4060
BAD_REQUEST = 4010
IP_BLOCKED = 4030
USER_NOT_FOUND = 4040
INVALID_TOKEN = 4060
INVALID_CODE = 4061
TOO_MANY_REQUEST = 4290
USER_NOT_ALLOW_TO_RECEIVE_SMS = 4291
# 5000
INTERNAL_SERVER_ERROR = 5000

INVALID_OTP = 4061

ERROR_TRANSLATION = {
    # 2000
    OK: "Ok",
    CREATED: "Created a row",
    # 4000
    INVALID_OTP: "Invalid code",
    TOO_MANY_REQUEST: "Please try again later",
    INVALID_TOKEN: "Invalid token",
    USER_NOT_FOUND: "User with this information not found",
    IP_BLOCKED: "Your IP address has been blocked and you will not be able"
                " to receive the code for a maximum of 24 hours.",
    USER_NOT_ALLOW_TO_RECEIVE_SMS: "You can only receive a code every two minutes",
    INVALID_CODE: "Invalid code",
    # 5000
    INTERNAL_SERVER_ERROR: "Interval server error",
}
