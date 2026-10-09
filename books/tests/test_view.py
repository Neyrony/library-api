from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from books.serializers import BookListRetrieveSerializer
from books.tests.test_base import BookTestData
from core.test_case_authenticated import APITestCaseAuthenticated, APITestCaseAdmin

LIST_URL = reverse("books:book-list")


def get_detailed_url(pk):
    return reverse("books:book-detail", kwargs={"pk": pk})


class UnauthenticatedUserTest(BookTestData, APITestCase):
    def test_forbidden_access(self):
        detailed_url = get_detailed_url(self.book.pk)

        response = self.client.post(LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(detailed_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(detailed_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(detailed_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        response = self.client.get(LIST_URL)

        all_books = Book.objects.all()
        books_serializer = BookListRetrieveSerializer(all_books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"], books_serializer.data)

    def test_retrieve(self):
        response = self.client.get(get_detailed_url(self.book.pk))

        book_serializer = BookListRetrieveSerializer(self.book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, book_serializer.data)


class AuthenticatedUserTest(BookTestData, APITestCaseAuthenticated):
    def test_forbidden_access(self):
        detailed_url = get_detailed_url(self.book.pk)

        response = self.client.post(LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(detailed_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(detailed_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(detailed_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_access(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(get_detailed_url(self.user.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdminTest(BookTestData, APITestCaseAdmin):
    def test_create(self):
        data = {
            "title": "book",
            "author": "author",
            "cover": "HARD",
            "inventory": 20,
            "daily_fee": "5.00",
        }

        response = self.client.post(LIST_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key, value in data.items():
            with self.subTest(key=key):
                self.assertEqual(response.data[key], value)

    def test_update(self):
        data = {
            "title": "new book",
            "author": "new author",
            "cover": "SOFT",
            "inventory": 20,
            "daily_fee": "1.00",
        }

        response = self.client.put(get_detailed_url(self.book.pk), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in data.items():
            with self.subTest(key=key):
                self.assertEqual(response.data[key], value)

    def test_partial_update(self):
        data = {
            "title": "new book",
        }

        response = self.client.patch(get_detailed_url(self.book.pk), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()

        self.assertEqual(data["title"], self.book.title)

    def test_destroy(self):
        response = self.client.delete(get_detailed_url(self.book.pk))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Book.DoesNotExist):
            self.book.refresh_from_db()
