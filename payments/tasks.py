import datetime
import os

import requests
from celery import shared_task
from django.utils import timezone

from payments.models import Payment

TELEGRAM_URL = (
    f"https://api.telegram.org/bot{os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage"
)


@shared_task
def check_expired_stripe_session():
    gap = timezone.now() - datetime.timedelta(days=1)
    pending_payments = Payment.objects.filter(status="PENDING", created_at__lte=gap)
    pending_payments.update(status="EXPIRED")


@shared_task
def telegram_notification_on_successful_payment(payment_pk):
    payment = Payment.objects.get(pk=payment_pk)

    requests.post(
        TELEGRAM_URL,
        json={
            "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
            "text": f"Successful payment:\n"
            f"Type: {payment.get_type_display()}\n"
            f"Borrowing: {str(payment.borrowing)}\n"
            f"Amount: {payment.money_to_pay}",
        },
    )
