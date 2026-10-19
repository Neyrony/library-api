from tokenize import TokenError

from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiRequest,
    inline_serializer,
    OpenApiResponse,
)
from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.serializers import UserSerializer, UserManageSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Create a new user",
        description="Create a new user with email and password in the system",
    ),
)
class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve a user",
    ),
    put=extend_schema(
        summary="Update an existing user",
    ),
    patch=extend_schema(
        summary="Partially update an existing user",
    ),
)
class UserManageView(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserManageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema_view(
    post=extend_schema(
        summary="Logout a user from the system",
        description="Put given refresh token in the blacklist",
        request=OpenApiRequest(
            request=inline_serializer(
                name="LogoutRequest", fields={"refresh_token": serializers.CharField()}
            ),
        ),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=inline_serializer(
                    name="LogoutErrorResponse",
                    fields={"error": serializers.CharField()},
                ),
                description="User successfully logged out, refresh token was moved into blacklist",
            ),
        },
    ),
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token", None)

        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                refresh_token.blacklist()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except TokenError:
                return Response(
                    {"error": "Invalid refresh token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema_view(
    post=extend_schema(
        summary="Give access and refresh tokens",
        description="Give access and refresh token to user by giver credentials",
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema_view(
    post=extend_schema(
        summary="Refresh access token",
        description="Give new access and refresh tokens by given refresh token",
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema_view(
    post=extend_schema(
        summary="Verify refresh token",
        description="Verify is refresh token valid or not",
    )
)
class CustomTokenVerifyView(TokenVerifyView):
    pass
