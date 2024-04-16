from django.contrib.auth import get_user_model

from rest_framework import serializers

from api import response_code
from api.response_code import ERROR_TRANSLATION
from api.serializers import BaseResponseSerializer, BaseResponseWithValidationErrorSerializer, \
    BaseResponseWithErrorSerializer
from authentication.validations import validate_phone_number

User = get_user_model()


class UserLoginByPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=128)


class AuthenticatedResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=32)

    class Meta:
        model = User
        fields = ("username", "phone_number", "email", "password")


class LoginByPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=11, max_length=11)

    def validate_phone_number(self, phone_number):
        return validate_phone_number(phone_number=phone_number)


class VerifySignUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=11, max_length=11)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_phone_number(self, phone_number):
        return validate_phone_number(phone_number=phone_number)


class LoginByPhoneNumberResponseSerializer(BaseResponseSerializer):
    pass


class LoginByPhoneNumberBadRequestSerializer(BaseResponseWithValidationErrorSerializer):
    error = LoginByPhoneNumberSerializer()


class IpBlockedErrorSerializer(BaseResponseWithErrorSerializer):
    code = serializers.IntegerField(default=response_code.IP_BLOCKED, min_value=4000, max_value=5999)
    error = serializers.CharField(default=ERROR_TRANSLATION[response_code.IP_BLOCKED])


class AuthFieldNotAllowedToReceiveSmsErrorSerializer(BaseResponseWithErrorSerializer):
    code = serializers.IntegerField(default=response_code.USER_NOT_ALLOW_TO_RECEIVE_SMS, min_value=4000, max_value=5999)
    error = serializers.CharField(default=ERROR_TRANSLATION[response_code.USER_NOT_ALLOW_TO_RECEIVE_SMS])


class VerifySignUserResponseSerializer(BaseResponseSerializer):
    result = AuthenticatedResponseSerializer()


class VerifySignUserBadRequestSerializer(BaseResponseWithValidationErrorSerializer):
    error = VerifySignUserSerializer()


class InvalidCodeErrSerializer(BaseResponseWithErrorSerializer):
    code = serializers.IntegerField(default=response_code.INVALID_CODE, min_value=4000, max_value=5999)
    error = serializers.CharField(default=ERROR_TRANSLATION[response_code.INVALID_CODE])


class RegisterResponseSerializer(BaseResponseSerializer):
    pass


class RegisterBadRequestSerializer(BaseResponseWithValidationErrorSerializer):
    error = RegisterSerializer()


class UserExistSerializer(BaseResponseWithErrorSerializer):
    code = serializers.IntegerField(default=response_code.USER_EXIST)
    error = serializers.CharField(default=ERROR_TRANSLATION[response_code.USER_EXIST])
