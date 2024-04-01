from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class RefreshAccessTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
