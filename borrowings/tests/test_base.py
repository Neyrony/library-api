from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from books.models import Book
from borrowings.models import Borrowing


class BorrowingTestData:
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
