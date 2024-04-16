from rest_framework import serializers

from api import response_code
from api.response_code import ERROR_TRANSLATION
from api.serializers import BaseResponseWithErrorSerializer, BaseResponseSerializer, \
    BaseResponseWithValidationErrorSerializer


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class RefreshAccessTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RefreshTokenBadRequest(BaseResponseWithValidationErrorSerializer):
    error = RefreshTokenSerializer()


class VerifyTokenResponseSerializer(BaseResponseSerializer):
    pass


class VerifyTokenBadRequestSerializer(BaseResponseWithValidationErrorSerializer):
    error = TokenSerializer()


class InvalidTokenSerializer(BaseResponseWithErrorSerializer):
    code = serializers.IntegerField(default=response_code.INVALID_TOKEN, min_value=4000, max_value=5999)
    error = serializers.CharField(default=ERROR_TRANSLATION[response_code.INVALID_TOKEN])


class RefreshAccessResponseSerializer(BaseResponseSerializer):
    result = AccessTokenSerializer()


class BanRefreshTokenResponseSerializer(BaseResponseSerializer):
    pass
