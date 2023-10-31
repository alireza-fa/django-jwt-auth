from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserLoginSerializer, UserRegisterSerializer
from .services import user_login_func, user_register_func


class UserLoginView(APIView):
    """
    The login function is the function that should do this:
        1. Get user information for login (such as email).
        2. Login the user or send a message confirming the account

        return:
            if user verify by password, return a Dictionary included(User Info, Tokens)
            if user verify by code or uuid, return None
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_login_func(request=request, phone_number=serializer.validated_data['phone_number'])
        except PermissionError as e:
            return Response(data={"detail": e}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    """
    The register function is the function that should do this:
        1. Get user information for register (such as phone number, email, password)
        2. send a message confirming the account

        return:
            return None
    """
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        try:
            user_register_func(request=request, phone_number=vd['phone_number'], fullname=vd['fullname'])
        except PermissionError as e:
            return Response(data={"detail": e}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_200_OK)


class UserVerifyView(APIView):
    """
    The verify function is the function that should be this:
        1. Get otp code or uuid
        2, verifying account

        return:
            return User info and Tokens
    """
    pass


class ResendVerifyMessage(APIView):
    """
    The resend verify message function is the function that should do this:
        1. Get Email or Phone number
        2. Check validate to resend verify message, else raise Exception
        3. send message

        return:
            return None
    """
    pass


class UserLogoutView(APIView):
    """
    The logout function is the function that should do this:
        1. Get Refresh token.
        2. check validate refresh token
        3. if refresh token is valid, it will be blacklisted. else raise Exception

        return:
            return None
    """
    pass


class JwtRefreshView(APIView):
    """
    The refresh token function is the function that should do this:
        1. Get Refresh token.
        2. check validate refresh token
        3. if refresh token is valid. return Access token, else raise Exception

        return:
            Access Token
    """
    pass


class JwtVerifyView(APIView):
    """
    The jwt verify function is the function that should do this:
        1. Get Token.
        2. if token is valid. return True, else return False.
    """
    pass
