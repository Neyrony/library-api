from django.contrib.auth import get_user_model
from django.test import TestCase


class TestCaseAuthenticated(TestCase):
    def setUp(self):
        super().setUp()
        user = get_user_model().objects.create_superuser(
            username="admin", email="admin@test.com", password="test12345"
        )
        self.client.force_login(user=user)
