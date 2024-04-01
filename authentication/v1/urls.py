from django.urls import path

from authentication.v1.views import sign_user, token

urlpatterns = [
    # sign
    path("login-by-password/", sign_user.UserLoginByPasswordView.as_view()),
    path("login/", sign_user.LoginByPhoneNumberView.as_view()),
    path("verify/", sign_user.VerifySignUserView.as_view()),
    path("register/", sign_user.RegisterView.as_view()),
    # token
    path("token/verify/", token.VerifyTokenView.as_view()),
    path("token/refresh/", token.RefreshAccessToken.as_view()),
    path("token/ban/", token.BanRefreshTokenView.as_view()),
]
