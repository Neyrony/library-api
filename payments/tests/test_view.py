from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from borrowings.models import Borrowing
from core.test_case_authenticated import APITestCaseAuthenticated, APITestCaseAdmin
from payments.models import Payment
from payments.serializers import PaymentListSerializer, PaymentRetrieveSerializer
from payments.tests.test_base import PaymentTestData

LIST_URL = reverse("payments:payment-list")


def get_detail_url(pk):
    return reverse("payments:payment-detail", kwargs={"pk": pk})


class UnauthenticatedUserTest(PaymentTestData, APITestCase):
    def test_forbidden_access(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(get_detail_url(self.payment.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(PaymentTestData, APITestCaseAuthenticated):
    def setUp(self):
        super().setUp()
        self.borrowing2 = Borrowing.objects.create(
            expected_return_date=timezone.localdate() + timedelta(days=1),
            book=self.book,
            user=self.user,
        )
        self.payment2 = Payment.objects.create(
            type="PAYMENT",
            borrowing=self.borrowing2,
            session_url="https://checkout.stripe.com/c/pay/test_token2",
            session_id="test_token2",
            money_to_pay=150,
        )

    def test_list(self):
        response = self.client.get(LIST_URL)

        payment2_serializer = PaymentListSerializer([self.payment2], many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], payment2_serializer.data)

    def test_retrieve(self):
        response = self.client.get(get_detail_url(self.payment.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(get_detail_url(self.payment2.id))

        payment2_serializer = PaymentRetrieveSerializer(self.payment2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, payment2_serializer.data)


class AdminUserTest(PaymentTestData, APITestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.borrowing2 = Borrowing.objects.create(
            expected_return_date=timezone.localdate() + timedelta(days=1),
            book=self.book,
            user=self.user,
        )
        self.payment2 = Payment.objects.create(
            type="PAYMENT",
            borrowing=self.borrowing2,
            session_url="https://checkout.stripe.com/c/pay/test_token2",
            session_id="test_token2",
            money_to_pay=150,
        )

    def test_forbidden_access(self):
        detail_url = get_detail_url(self.payment2.id)

        response = self.client.post(LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(detail_url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(detail_url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list(self):
        response = self.client.get(LIST_URL)

        payment2_serializer = PaymentListSerializer(Payment.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"], payment2_serializer.data)

    def test_retrieve(self):
        response = self.client.get(get_detail_url(self.payment.id))

        payment_serializer = PaymentRetrieveSerializer(self.payment)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, payment_serializer.data)

        response = self.client.get(get_detail_url(self.payment2.id))

        payment2_serializer = PaymentRetrieveSerializer(self.payment2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, payment2_serializer.data)
