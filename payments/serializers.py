from rest_framework import serializers

from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingPaymentRetrieveSerializer,
)
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentListSerializer(PaymentSerializer):
    status = serializers.CharField(read_only=True, source="get_status_display")
    type = serializers.CharField(read_only=True, source="get_type_display")
    borrowing = BorrowingListSerializer(read_only=True)


class PaymentRetrieveSerializer(PaymentSerializer):
    status = serializers.CharField(read_only=True, source="get_status_display")
    type = serializers.CharField(read_only=True, source="get_type_display")
    borrowing = BorrowingPaymentRetrieveSerializer(read_only=True)
