from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserRegisterAPIViewSet,
    UpdatePassword,
    Logout,
)

urlpatterns = [
    path("v1/register/", UserRegisterAPIViewSet.as_view(), name="register_api"),
    path("v1/login/", obtain_auth_token),
    path("v1/logout/", Logout.as_view()),
    path("v1/change/password/", UpdatePassword.as_view(), name="change_pass_api"),
]
