from rest_framework import serializers

from api import response_code
from api.response_code import ERROR_TRANSLATION
from api.serializers import BaseResponseWithErrorSerializer


class UserNotFoundErrorSerializer(BaseResponseWithErrorSerializer):
    code = serializers.IntegerField(default=response_code.USER_NOT_FOUND)
    error = serializers.CharField(default=ERROR_TRANSLATION[response_code.USER_NOT_FOUND])
