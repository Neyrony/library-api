from django.urls import reverse

from core.test_case_authenticated import TestCaseAuthenticated
from user.tests.test_base import UserTestData


class UserAdminTest(UserTestData, TestCaseAuthenticated):

    def test_display(self):
        response = self.client.get(reverse("admin:user_user_changelist"))

        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.is_staff)
