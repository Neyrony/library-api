from django.urls import path

from user.views import (
    UserCreateView,
    UserManageView,
    LogoutView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
)

urlpatterns = [
    path("", UserCreateView.as_view(), name="register"),
    path("me/", UserManageView.as_view(), name="profile"),
    path("token/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="refresh"),
    path("token/verify/", CustomTokenVerifyView.as_view(), name="verify"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

app_name = "user"
