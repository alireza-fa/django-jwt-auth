from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginByPasswordSerializer, TokenVerifySerializer, RefreshTokenSerializer, ProfileSerializer
from .token import generate_token, refresh_access_token
from .exceptions import TokenError

User = get_user_model()


class LoginByPasswordView(APIView):
    serializer_class = LoginByPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        try:
            user = User.objects.get(username=vd["username"])
        except User.DoesNotExist:
            return Response(data={"error": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(vd["password"]):
            return Response(data={"error": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        token = generate_token(request=request, user=user)

        return Response(data=token, status=status.HTTP_200_OK)


class TokenVerifyView(APIView):
    serializer_class = TokenVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            access_token = refresh_access_token(request=request, raw_refresh_token=serializer.validated_data["refresh_token"])
        except TokenError:
            return Response(data={"error": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"access_token": access_token}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request):
        serializer = self.serializer_class(instance=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
