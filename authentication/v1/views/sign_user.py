from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView

from accounts.serializers.user import UserNotFoundErrorSerializer
from api import response_code
from api.response import base_response_with_error, base_response, base_response_with_validation_error
from authentication.v1.services.sign_user import register_user, login_by_phone_number, verify_sign_user, \
    login_by_password
from authentication.v1.serializers.sign_user import RegisterSerializer, \
    LoginByPhoneNumberSerializer, VerifySignUserSerializer, IpBlockedErrorSerializer, \
    AuthFieldNotAllowedToReceiveSmsErrorSerializer, LoginByPhoneNumberResponseSerializer, \
    LoginByPhoneNumberBadRequestSerializer, VerifySignUserResponseSerializer, VerifySignUserBadRequestSerializer, \
    InvalidCodeErrSerializer, RegisterResponseSerializer, RegisterBadRequestSerializer, UserExistSerializer, \
    UserLoginByPasswordSerializer, AuthenticatedResponseSerializer
from authentication import exceptions
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.utils import OpenApiRequest, OpenApiResponse

from api.swagger_fields import PHONE_NUMBER_DESCRIPTION, REGISTER_EXAMPLE_VALUE, \
    LOGIN_BY_PHONE_NUMBER_EXAMPLE_VALUE, LOGIN_BY_PHONE_NUMBER_200_DESCRIPTION, IP_BLOCKED_DESCRIPTION, \
    VERIFY_SIGN_EXAMPLE_VALUE, OTP_CODE_DESCRIPTION, USERNAME_DESCRIPTION, REGISTER_200_DESCRIPTION

SCHEMA_TAGS = ("Auth",)
User = get_user_model()


class UserLoginByPasswordView(APIView):
    serializer_class = UserLoginByPasswordSerializer

    @extend_schema(request=UserLoginByPasswordSerializer, responses=AuthenticatedResponseSerializer, tags=SCHEMA_TAGS)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                token = login_by_password(request=request, username=serializer.validated_data["username"],
                                          password=serializer.validated_data["password"])
            except User.DoesNotExist:
                return base_response_with_error(status_code=status.HTTP_404_NOT_FOUND,
                                                code=response_code.USER_NOT_FOUND)

            return base_response(status_code=status.HTTP_200_OK, code=response_code.OK, result=token)

        return base_response_with_validation_error(error=serializer.errors)


class LoginByPhoneNumberView(APIView):
    serializer_class = LoginByPhoneNumberSerializer

    @extend_schema(
        request=OpenApiRequest(request=LoginByPhoneNumberSerializer, examples=[
            OpenApiExample(name="phone_number", value=LOGIN_BY_PHONE_NUMBER_EXAMPLE_VALUE, description=PHONE_NUMBER_DESCRIPTION)]),
        responses={
            200: OpenApiResponse(response=LoginByPhoneNumberResponseSerializer, description=LOGIN_BY_PHONE_NUMBER_200_DESCRIPTION),
            400: OpenApiResponse(response=LoginByPhoneNumberBadRequestSerializer, description="bad request"),
            403: OpenApiResponse(response=IpBlockedErrorSerializer, description=IP_BLOCKED_DESCRIPTION),
            404: OpenApiResponse(response=UserNotFoundErrorSerializer),
            429: OpenApiResponse(response=AuthFieldNotAllowedToReceiveSmsErrorSerializer)},
        tags=SCHEMA_TAGS)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                login_by_phone_number(request=request, phone_number=serializer.validated_data["phone_number"])
            except exceptions.IpBlocked:
                return base_response_with_error(status_code=status.HTTP_403_FORBIDDEN, code=response_code.IP_BLOCKED)
            except User.DoesNotExist:
                return base_response_with_error(status_code=status.HTTP_404_NOT_FOUND, code=response_code.USER_NOT_FOUND)
            except exceptions.AuthFieldNotAllowedToReceiveSms:
                return base_response_with_error(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                                code=response_code.USER_NOT_ALLOW_TO_RECEIVE_SMS)

            return base_response(status_code=status.HTTP_200_OK, code=response_code.OK)

        return base_response_with_validation_error(error=serializer.errors)


class VerifySignUserView(APIView):
    serializer_class = VerifySignUserSerializer

    @extend_schema(
        request=OpenApiRequest(request=VerifySignUserSerializer, examples=[
            OpenApiExample(name="code", value=VERIFY_SIGN_EXAMPLE_VALUE, description=OTP_CODE_DESCRIPTION,),
            OpenApiExample(name="phone_number", value=VERIFY_SIGN_EXAMPLE_VALUE, description=PHONE_NUMBER_DESCRIPTION)]),
        responses={
            200: OpenApiResponse(response=VerifySignUserResponseSerializer),
            400: OpenApiResponse(response=VerifySignUserBadRequestSerializer),
            404: OpenApiResponse(response=UserNotFoundErrorSerializer),
            406: OpenApiResponse(response=InvalidCodeErrSerializer),
            409: OpenApiResponse(response=UserExistSerializer),
        },
        tags=SCHEMA_TAGS)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            try:
                token = verify_sign_user(request=request, phone_number=vd["phone_number"], code=vd["code"])
            except exceptions.InvalidCode:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                code=response_code.INVALID_CODE)
            except User.DoesNotExist:
                return base_response_with_error(status_code=status.HTTP_404_NOT_FOUND, code=response_code.USER_NOT_FOUND)
            except ValidationError:
                return base_response_with_error(status_code=status.HTTP_409_CONFLICT,
                                                code=response_code.USER_EXIST)

            return base_response(status_code=status.HTTP_200_OK, code=response_code.OK, result=token)

        return base_response_with_validation_error(error=serializer.errors)


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        request=OpenApiRequest(request=RegisterSerializer, examples=[
            OpenApiExample(name="username", value=REGISTER_EXAMPLE_VALUE, description=USERNAME_DESCRIPTION),
            OpenApiExample(name="phone_number", value=REGISTER_EXAMPLE_VALUE, description=PHONE_NUMBER_DESCRIPTION)]),
        responses={
            200: OpenApiResponse(response=RegisterResponseSerializer, description=REGISTER_200_DESCRIPTION),
            400: OpenApiResponse(response=RegisterBadRequestSerializer),
            403: OpenApiResponse(response=IpBlockedErrorSerializer, description=IP_BLOCKED_DESCRIPTION),
            429: OpenApiResponse(response=AuthFieldNotAllowedToReceiveSmsErrorSerializer)
        },
        tags=SCHEMA_TAGS)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                register_user(request=request, **serializer.validated_data)
            except exceptions.AuthFieldNotAllowedToReceiveSms:
                return base_response_with_error(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                                code=response_code.USER_NOT_ALLOW_TO_RECEIVE_SMS)
            except exceptions.IpBlocked:
                return base_response_with_error(status_code=status.HTTP_403_FORBIDDEN, code=response_code.IP_BLOCKED)

            return base_response(status_code=status.HTTP_200_OK, code=response_code.OK)

        return base_response_with_validation_error(error=serializer.errors)
