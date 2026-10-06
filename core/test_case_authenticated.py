from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APITestCase


class TestCaseAuthenticated(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test12345"
        )
        self.client.force_login(user=self.user)


class APITestCaseAuthenticated(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            email="regular_user@test.com", password="test12345"
        )
        self.client.force_authenticate(user=self.user)


class APITestCaseAdmin(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test12345"
        )
        self.client.force_authenticate(user=self.user)
