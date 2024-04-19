from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.LoginByPasswordView.as_view()),
    path("token/verify/", views.TokenVerifyView.as_view()),
    path("token/refresh/", views.TokenRefreshView.as_view()),
    path("profile/", views.ProfileView.as_view()),
]
