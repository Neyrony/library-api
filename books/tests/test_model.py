from django.test import TestCase

from books.tests.test_base import BookTestData


class TestModel(BookTestData, TestCase):
    def test_str(self):
        self.assertEqual(str(self.book), f"{self.book.title} ({self.book.author})")
