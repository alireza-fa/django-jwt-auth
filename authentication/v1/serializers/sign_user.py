from django.contrib.auth import get_user_model

from rest_framework import serializers

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
