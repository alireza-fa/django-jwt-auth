from rest_framework import serializers

from api import response_code
from api.response_code import ERROR_TRANSLATION


class BaseResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    code = serializers.IntegerField(default=2000, min_value=1000, max_value=3999)


class BaseResponseWithErrorSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False)


class BaseResponseWithValidationErrorSerializer(serializers.Serializer):
    code = serializers.IntegerField(default=4001)
    success = serializers.BooleanField(default=False)


class InternalServerErrSerializer(BaseResponseWithErrorSerializer):
    code = serializers.IntegerField(default=response_code.INTERNAL_SERVER_ERROR)
    error = serializers.CharField(default=ERROR_TRANSLATION[response_code.INTERNAL_SERVER_ERROR])
