import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from borrowings.models import Borrowing

TELEGRAM_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"


@shared_task
def send_telegram_borrowing_notification(pk):
    borrowing = Borrowing.objects.get(pk=pk)

    data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": f"Borrowing was created at {borrowing.borrow_date}\n"
        f"It is expected to return at {borrowing.expected_return_date}\n"
        f"Book: {str(borrowing.book)}\n"
        f"User: {borrowing.user}\n",
    }

    requests.post(
        TELEGRAM_URL,
        json=data,
    )


@shared_task
def daily_overdue_borrowing_notification():
    overdue_borrowing = Borrowing.objects.filter(
        expected_return_date__lt=timezone.localtime(), actual_return_date__isnull=True
    ).values_list("id", flat=True)

    if overdue_borrowing:
        requests.post(
            TELEGRAM_URL,
            json={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": "List of all overdue borrowings for today",
            },
        )

        for borrow_id in overdue_borrowing:
            send_telegram_borrowing_notification.delay(borrow_id)
    else:
        requests.post(
            TELEGRAM_URL,
            json={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": "No borrowings overdue today!",
            },
        )
