import os

import stripe
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    inline_serializer,
    OpenApiRequest,
    OpenApiResponse,
)
from rest_framework import mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from payments.models import Payment
from payments.serializers import (
    PaymentListSerializer,
    PaymentRetrieveSerializer,
    PaymentSerializer,
)
from payments.services import get_or_update_stripe_session_url
from payments.tasks import telegram_notification_on_successful_payment


@extend_schema_view(
    list=extend_schema(
        summary="Shows a list of payment",
        description="Shows a list of user's payment or "
        "if user is admin shows all payments",
    ),
    retrieve=extend_schema(
        summary="Shows detailed information about payment",
        description="Shows detailed information only about user's payment "
        "but user can not check other payments if he is not admin",
    ),
    webhook=extend_schema(
        summary="Receive data from stripe",
        description="Receive post response from stripe with detailed information "
        "about user's payment and proceed it",
        request=OpenApiRequest(
            request=inline_serializer(
                name="StripeWebhookSerializer",
                fields={
                    "id": serializers.CharField(),
                    "type": serializers.CharField(),
                    "data": serializers.JSONField(),
                },
            )
        ),
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=inline_serializer(
                    name="StripeWebhookErrorSerializer",
                    fields={
                        "error": serializers.CharField(),
                    },
                ),
                description="Payment was not successful",
            ),
            status.HTTP_404_NOT_FOUND: None,
        },
    ),
    success=extend_schema(
        summary="Shows information that payment was successful",
        request=None,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=inline_serializer(
                    name="SuccessPaymentSerializer",
                    fields={
                        "details": serializers.CharField(),
                    },
                ),
                description="Payment was successful. Your order is being processed",
            ),
        },
    ),
    cancel=extend_schema(
        summary="Shows information that payment was cancelled and "
        "user can complete it later",
        request=None,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=inline_serializer(
                    name="CancelPaymentSerializer",
                    fields={
                        "details": serializers.CharField(),
                    },
                ),
                description="Payment was cancelled. You can complete it later",
            )
        },
    ),
)
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
            return PaymentRetrieveSerializer
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

            telegram_notification_on_successful_payment.delay(payment.id)

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def success(self, request):
        return Response(
            {"details": "Payment was successful. Your order is being processed"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["GET"])
    def cancel(self, request):
        return Response(
            {"details": "Payment was cancelled. You can complete it later"},
            status=status.HTTP_200_OK,
        )
