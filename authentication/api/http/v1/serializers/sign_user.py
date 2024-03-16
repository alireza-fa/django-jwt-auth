from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserLoginByPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=128)


class AuthenticatedResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "phone_number", "password")
