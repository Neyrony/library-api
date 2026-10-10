import requests
from celery import shared_task
from django.conf import settings

from borrowings.models import Borrowing


@shared_task
def send_telegram_borrowing_notification(pk):
    borrowing = Borrowing.objects.get(pk=pk)

    chat_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": f"Borrowing was created at {borrowing.borrow_date}\n"
        f"It is expected to return at {borrowing.expected_return_date}\n"
        f"Book: {str(borrowing.book)}\n"
        f"User: {borrowing.user}\n",
    }

    requests.post(
        chat_url,
        json=data,
    )
