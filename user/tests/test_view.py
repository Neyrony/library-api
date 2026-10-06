from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from core.test_case_authenticated import APITestCaseAdmin
from user.serializers import UserManageSerializer


class UnauthenticatedUserTest(APITestCase):
    def test_forbidden_access(self):
        response = self.client.get(reverse("user:profile"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register(self):
        data = {"email": "user@test.com", "password": "test12345"}
        response = self.client.post(
            reverse("user:register"),
            data=data,
        )

        user = get_user_model().objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))


class AuthenticatedUserTest(APITestCaseAdmin):
    def test_profile_get(self):
        response = self.client.get(reverse("user:profile"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_serializer = UserManageSerializer(self.user)

        self.assertEqual(response.data, user_serializer.data)

    def test_profile_put(self):
        data = {
            "email": "new_user@test.com",
            "password": "test54321",
            "first_name": "new first name",
            "last_name": "new last name",
        }

        response = self.client.put(reverse("user:profile"), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        for key, value in data.items():
            with self.subTest(key=key):
                if key != "password":
                    self.assertEqual(response.data[key], value)

        self.assertTrue(self.user.check_password(data["password"]))

    def test_profile_patch(self):
        data = {
            "email": "new_user@test.com",
        }

        response = self.client.patch(reverse("user:profile"), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["email"], data["email"])

    def test_logout(self):
        refresh_token = RefreshToken.for_user(self.user)

        response = self.client.post(
            reverse("user:logout"), data={"refresh_token": str(refresh_token)}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(TokenError):
            refresh_token.check_blacklist()
