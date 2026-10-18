from django.test import TestCase

from payments.tests.test_base import PaymentTestData


class TestModel(PaymentTestData, TestCase):
    def test_str(self):
        self.assertEqual(
            str(self.payment),
            f"{str(self.payment.borrowing)} - {self.payment.get_status_display()}",
        )
