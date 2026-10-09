from books.models import Book


class BookTestData:
    @classmethod
    def setUpTestData(cls) -> None:
        cls.book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=10, daily_fee=1
        )
