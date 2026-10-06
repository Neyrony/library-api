from django.test import TestCase

from books.models import Book


class TestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title="title", author="author", inventory=3, daily_fee=3.2
        )

    def test_str(self):
        self.assertEqual(str(self.book), f"{self.book.title} ({self.book.author})")
