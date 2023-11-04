from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (UserLoginSerializer, UserRegisterSerializer,
                          UserVerifySerializer, ResendVerifyMessageSerializer,
                          RefreshTokenSerializer, TokenSerializer,)
from .services import (user_login_func, user_register_func, user_verify_func,
                       user_resend_func, refresh_token_func, check_verify_token_func,
                       user_logout_func,)


class UserLoginView(APIView):
    """
    The login function is the function that should do this:
        1. Get user information for login (such as email).
        2. Login the user or send a message confirming the account

        return:
            if user verify by password, return a Dictionary included(User Info, Tokens)
            if user verify by code or uuid, return None
        Note:
            If registration is done only with (mobile number or email), then login and register are done in one view
             and function.
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_login_func(request=request, phone_number=serializer.validated_data['phone_number'])
        except PermissionError:
            return Response(data={"detail": _('Please try again later')}, status=status.HTTP_406_NOT_ACCEPTABLE)
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
        except PermissionError:
            return Response(data={"detail": _('Please try again later.')}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_200_OK)


class UserVerifyView(APIView):
    """
    The verify function is the function that should be this:
        1. Get otp code or uuid
        2, verifying account

        return:
            return User info and Tokens
    """
    serializer_class = UserVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        try:
            data = user_verify_func(request=request, code=vd['code'], phone_number=vd['phone_number'])
        except ValueError:
            return Response(data={"detail": _('Invalid code')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=data, status=status.HTTP_200_OK)


class ResendVerifyMessage(APIView):
    """
    The resend verify message function is the function that should do this:
        1. Get Email or Phone number
        2. Check validate to resend verify message, else raise Exception
        3. send message

        return:
            return None
    """
    serializer_class = ResendVerifyMessageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_resend_func(request=request, phone_number=serializer.validated_data['phone_number'])
        except PermissionError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_200_OK)


class JwtRefreshView(APIView):
    """
    The refresh token function is the function that should do this:
        1. Get Refresh token.
        2. check validate refresh token
        3. if refresh token is valid. return Access token, else raise Exception

        return:
            Access Token
    """
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            access_token = refresh_token_func(
                request=request,
                encrypted_refresh_token=serializer.validated_data['refresh_token'])
        except ValueError:
            return Response(
                data={"refresh_token": _('Invalid refresh token.')},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"access_token": access_token}, status=status.HTTP_200_OK)


class JwtVerifyView(APIView):
    """
    The jwt verify function is the function that should do this:
        1. Get Token.
        2. if token is valid. return True, else return False.
    """
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        check = check_verify_token_func(
            request=request, encrypted_token=serializer.validated_data['token'])
        if check is False:
            return Response(data={"token": _('Invalid token')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
    The logout function is the function that should do this:
        1. Get Refresh token.
        2. check validate refresh token
        3. if refresh token is valid, it will be blacklisted. else raise Exception

        return:
            return None
    """
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_logout_func(request=request, encrypted_token=serializer.validated_data['token'])
        except ValueError:
            return Response(data={"token": _('Invalid token.')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
