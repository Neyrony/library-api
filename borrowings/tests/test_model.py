from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from books.models import Book
from borrowings.models import Borrowing


class TestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title="title", author="author", inventory=3, daily_fee=3.2
        )
        cls.user = get_user_model().objects.create_user(
            email="user@example.com", password="test12345"
        )
        cls.borrowing = Borrowing.objects.create(
            expected_return_date=timezone.localdate() + timedelta(days=1),
            user=cls.user,
            book=cls.book,
        )

    def test_str(self):
        self.assertEqual(
            str(self.borrowing),
            f"{self.borrowing.book.title} ({self.borrowing.borrow_date})",
        )

    def test_date_validation(self):
        with self.assertRaises(ValidationError):
            Borrowing.objects.create(
                expected_return_date=timezone.localdate() + timedelta(days=2),
                user=self.user,
                book=self.book,
                actual_return_date=timezone.localdate() + timedelta(days=1),
            )

        with self.assertRaises(ValidationError):
            Borrowing.objects.create(
                expected_return_date=timezone.localdate() - timedelta(days=2),
                user=self.user,
                book=self.book,
            )

        with self.assertRaises(ValidationError):
            self.borrowing.expected_return_date = timezone.localdate() + timedelta(
                days=3
            )
            self.borrowing.save()

        with self.assertRaises(ValidationError):
            self.borrowing.actual_return_date = timezone.localdate() - timedelta(days=3)
            self.borrowing.save()

        with self.assertRaises(ValidationError):
            self.borrowing.actual_return_date = timezone.localdate() + timedelta(days=3)
            self.borrowing.save()
            self.borrowing.actual_return_date = timezone.localdate() + timedelta(days=4)
            self.borrowing.save()

    def test_user_and_book_validation(self):
        with self.assertRaises(ValidationError):
            book = Book.objects.create(
                title="title2", author="author2", inventory=5, daily_fee=3.2
            )
            self.borrowing.book = book
            self.borrowing.save()

        with self.assertRaises(ValidationError):
            user = get_user_model().objects.create_user(
                email="user2@example.com", password="test12345"
            )
            self.borrowing.user = user
            self.borrowing.save()
