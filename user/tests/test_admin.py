from django.contrib.auth import get_user_model
from django.urls import reverse

from core.test_case_authenticated import TestCaseAuthenticated


class UserAdminTest(TestCaseAuthenticated):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create(
            email="user@example.com",
            password="test12345",
            first_name="regular",
            last_name="user",
        )

    def test_display(self):
        response = self.client.get(reverse("admin:user_user_changelist"))

        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.is_staff)
