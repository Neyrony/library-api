from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import UserCreateView, UserManageView, LogoutView

urlpatterns = [
    path("", UserCreateView.as_view(), name="register"),
    path("me/", UserManageView.as_view(), name="profile"),
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify"),
    path("logout/", LogoutView.as_view(), name="logout")
]

app_name = "user"
