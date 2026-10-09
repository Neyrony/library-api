from datetime import timedelta

from django.urls import reverse
from django.utils import dateformat

from borrowings.tests.test_base import BorrowingTestData
from core.test_case_authenticated import TestCaseAuthenticated


class BorrowingAdminTest(BorrowingTestData, TestCaseAuthenticated):
    def test_display(self):
        self.borrowing.actual_return_date = self.borrowing.borrow_date + timedelta(
            days=1
        )
        self.borrowing.save()

        response = self.client.get(reverse("admin:borrowings_borrowing_changelist"))

        self.assertContains(
            response, dateformat.format(self.borrowing.borrow_date, "N j, Y")
        )
        self.assertContains(
            response, dateformat.format(self.borrowing.expected_return_date, "N j, Y")
        )
        self.assertContains(
            response, dateformat.format(self.borrowing.actual_return_date, "N j, Y")
        )
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.book.title)
