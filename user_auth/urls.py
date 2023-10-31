from django.urls import path

from . import views


app_name = 'user_auth'


urlpatterns = [
    path('login/', views.UserLoginView.as_view()),
    path('register/', views.UserRegisterView.as_view()),
    path('verify/', views.UserVerifyView.as_view()),
    path('verify/resend/', views.ResendVerifyMessage.as_view()),
    path('token/refresh/', views.JwtRefreshView.as_view()),
    path('token/verify/', views.JwtVerifyView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),
]
