from rest_framework import serializers
from django.contrib.auth import get_user_model

from .token import verify_token, refresh_access_token


User = get_user_model()


class LoginByPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        if not verify_token(request=self.context["request"], raw_token=token):
            raise serializers.ValidationError("Invalid token")
        return token


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email")
