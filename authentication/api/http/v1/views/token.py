from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ..serializers.token import TokenSerializer, RefreshAccessTokenSerializer, RefreshTokenSerializer
from authentication.services.token import verify_token, refresh_access_token, ban_token
from api.response import base_response, base_response_with_error, base_response_with_validation_error
from api import response_code

User = get_user_model()


class VerifyTokenView(APIView):
    serializer_class = TokenSerializer

    @extend_schema(request=TokenSerializer, responses=None)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token_verified = verify_token(request=request, token=serializer.validated_data["token"])

            if not token_verified:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                code=response_code.INVALID_TOKEN)

            return base_response(status_code=status.HTTP_200_OK, code=response_code.OK)

        return base_response_with_validation_error(error=serializer.errors)


class RefreshAccessToken(APIView):
    serializer_class = RefreshAccessTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                access_token = refresh_access_token(request=request, refresh_token=serializer.validated_data["refresh_token"])
            except ValueError:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                code=response_code.INVALID_TOKEN)
            except User.DoesNotExist:
                return base_response_with_error(status_code=status.HTTP_404_NOT_FOUND, code=response_code.USER_NOT_FOUND)

            return base_response(status_code=status.HTTP_200_OK, code=response_code.OK,
                                 result={"access_token": access_token})

        return base_response_with_validation_error(error=serializer.errors)


class BanRefreshTokenView(APIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                ban_token(encrypted_token=serializer.validated_data["refresh_token"])
            except ValueError:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                code=response_code.INVALID_TOKEN)

            return base_response(status_code=status.HTTP_200_OK, code=response_code.OK)

        return base_response_with_validation_error(error=serializer.errors)
