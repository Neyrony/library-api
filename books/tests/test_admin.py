from django.urls import reverse

from books.models import Book
from core.test_case_authenticated import TestCaseAuthenticated


class BookAdminTest(TestCaseAuthenticated):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.book = Book.objects.create(
            title="title", author="author", cover="HARD", inventory=15, daily_fee=1
        )

    def test_book_display(self):
        response = self.client.get(reverse("admin:books_book_changelist"))

        self.assertContains(response, self.book.title)
        self.assertContains(response, self.book.author)
        self.assertContains(response, self.book.cover)
        self.assertContains(response, self.book.inventory)
        self.assertContains(response, str(self.book.daily_fee))
