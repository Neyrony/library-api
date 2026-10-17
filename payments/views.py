import os

import stripe
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from payments.models import Payment
from payments.serializers import (
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentSerializer,
)
from payments.services import get_or_update_stripe_session_url


class PaymentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Payment.objects.all()
        else:
            queryset = Payment.objects.filter(borrowing__user=self.request.user)

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("borrowing__book", "borrowing__user")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        elif self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = get_or_update_stripe_session_url(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def webhook(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        secret_key = os.getenv("STRIPE_WEBHOOK_SECRET")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, secret_key)
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "checkout.session.completed":
            session_id = event["data"]["object"]["id"]

            try:
                payment = Payment.objects.get(session_id=session_id)
            except Payment.DoesNotExist:
                return Response(
                    {"error": "Payment does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            payment.status = "PAID"
            payment.save()

        return Response(status=status.HTTP_200_OK)
