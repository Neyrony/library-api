from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingRetrieveSerializer
from borrowings.tests.test_base import BorrowingTestData
from core.test_case_authenticated import APITestCaseAuthenticated, APITestCaseAdmin

LIST_URL = reverse("borrowings:borrowing-list")


def get_detailed_url(pk):
    return reverse("borrowings:borrowing-detail", kwargs={"pk": pk})


class UnauthenticatedUserTest(BorrowingTestData, APITestCase):
    def test_forbidden_access(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(get_detailed_url(self.borrowing.pk))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(
            reverse("borrowings:borrowing-return", kwargs={"pk": self.borrowing.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(BorrowingTestData, APITestCaseAuthenticated):
    def setUp(self):
        super().setUp()
        self.borrowing1 = Borrowing.objects.create(
            expected_return_date=timezone.localdate() + timedelta(days=4),
            user=self.user,
            book=self.book,
        )

    def test_list(self):
        response = self.client.get(LIST_URL)

        borrowing1_serializer = BorrowingListSerializer([self.borrowing1], many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], borrowing1_serializer.data)

    def test_retrieve(self):
        response = self.client.get(get_detailed_url(self.borrowing.pk))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(get_detailed_url(self.borrowing1.pk))

        borrowing_serializer = BorrowingRetrieveSerializer(self.borrowing1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, borrowing_serializer.data)

    @freeze_time("2026-10-9")
    def test_create(self):
        data = {
            "expected_return_date": timezone.localdate() + timedelta(days=1),
            "book": self.book.pk,
        }
        borrow_date = timezone.localdate()
        response = self.client.post(
            LIST_URL,
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.data["expected_return_date"],
            data["expected_return_date"].strftime("%Y-%m-%d"),
        )
        self.assertEqual(response.data["book"], data["book"])
        self.assertEqual(response.data["borrow_date"], borrow_date.strftime("%Y-%m-%d"))


class AdminUserTest(BorrowingTestData, APITestCaseAdmin):
    def test_forbidden_access(self):
        response = self.client.put(get_detailed_url(self.borrowing.pk))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(get_detailed_url(self.borrowing.pk))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(get_detailed_url(self.borrowing.pk))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_return(self):
        response = self.client.get(get_detailed_url(self.borrowing.pk))

        self.borrowing.refresh_from_db()

        borrowing_serializer = BorrowingRetrieveSerializer(self.borrowing)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, borrowing_serializer.data)
