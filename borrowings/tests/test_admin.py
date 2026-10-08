from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone, dateformat

from books.models import Book
from borrowings.models import Borrowing
from core.test_case_authenticated import TestCaseAuthenticated


class BorrowingAdminTest(TestCaseAuthenticated):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title="title", author="author", inventory=3, daily_fee=3.2
        )
        cls.user = get_user_model().objects.create_user(
            email="user@example.com", password="test12345"
        )
        cls.borrowing = Borrowing.objects.create(
            expected_return_date=timezone.localdate() + timedelta(days=3),
            user=cls.user,
            book=cls.book,
        )

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
