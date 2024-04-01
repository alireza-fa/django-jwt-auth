from django.urls import path, include

v1 = [
    path("auth/", include("authentication.v1.urls"))
]

urlpatterns = [
    path("v1/", include(v1))
]
