from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .validations import validate_phone_number, persian_to_english


User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=16)

    def validate_phone_number(self, value):
        phone_number = validate_phone_number(phone_number=value)

        users = User.objects.filter(phone_number=phone_number)
        if not users.exists():
            raise serializers.ValidationError(_('User with this phone number not exist.'))

        return phone_number


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'fullname')

    def validate_phone_number(self, value):
        return validate_phone_number(phone_number=value)

    def validate_email(self, email):
        if email:
            users = User.objects.filter(email=email)
            if users.exists():
                return serializers.ValidationError(_('User with this email already exist.'))
        return email


class UserVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=16)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_phone_number(self, value):
        return validate_phone_number(phone_number=value)

    def validate_code(self, value):
        return persian_to_english(number=value)


class UserVerifyResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    profile = serializers.SerializerMethodField()


class ResendVerifyMessageSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=16)

    def validate_phone_number(self, value):
        return validate_phone_number(phone_number=value)


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
