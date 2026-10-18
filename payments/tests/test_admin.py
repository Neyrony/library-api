from django.urls import reverse
from django.utils import dateformat, timezone

from core.test_case_authenticated import TestCaseAuthenticated
from payments.tests.test_base import PaymentTestData


class BorrowingAdminTest(PaymentTestData, TestCaseAuthenticated):
    def test_display(self):
        response = self.client.get(reverse("admin:payments_payment_changelist"))

        self.assertContains(response, self.payment.get_status_display())
        self.assertContains(response, self.payment.get_type_display())
        self.assertContains(response, str(self.payment.borrowing))
        self.assertContains(response, self.payment.session_url)
        self.assertContains(response, self.payment.session_id)
        self.assertContains(response, self.payment.money_to_pay)
        self.assertContains(
            response, dateformat.format(timezone.localtime(self.payment.created_at), "N j, Y, g:i a")
        )
