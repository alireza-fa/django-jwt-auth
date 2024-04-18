class BaseJWTException(Exception):
    pass


class CheckClaimsErr(BaseJWTException):
    pass


class TokenError(Exception):
    pass
