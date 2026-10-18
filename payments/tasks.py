import datetime

from celery import shared_task
from django.utils import timezone

from payments.models import Payment


@shared_task
def check_expired_stripe_session():
    gap = timezone.now() - datetime.timedelta(days=1)
    pending_payments = Payment.objects.filter(status="PENDING", created_at__lte=gap)
    pending_payments.update(status="EXPIRED")
