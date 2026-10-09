from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingSerializer,
    EmptySerializer,
)


class BorrowingsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _str_to_list_int(string):
        try:
            return [int(pk) for pk in string.split(",") if pk]
        except ValueError:
            return []

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("user", "book")

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if self.action == "list":
            is_active = self.request.query_params.get("is_active")
            user_id = self.request.query_params.get("user_id")

            if is_active:
                if is_active.lower().strip() == "true":
                    queryset = queryset.filter(actual_return_date__isnull=True)
                elif is_active.lower().strip() == "false":
                    queryset = queryset.filter(actual_return_date__isnull=False)

            if user_id and self.request.user.is_staff:
                user_id_list = self._str_to_list_int(user_id)

                queryset = queryset.filter(user_id__in=user_id_list)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action == "retrieve":
            return BorrowingRetrieveSerializer
        elif self.action == "return_book":
            return EmptySerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["POST"],
        url_path="return",
        url_name="return",
        permission_classes=[IsAdminUser],
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if getattr(borrowing, "actual_return_date", None) is not None:
            return Response(
                {"error": "You can not return book, if it is already returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            borrowing.actual_return_date = timezone.localdate()
            borrowing.save()
            borrowing.book.increase_inventory()

        borrowing_serializer = BorrowingRetrieveSerializer(
            borrowing, context=self.get_serializer_context()
        )

        return Response(borrowing_serializer.data, status=status.HTTP_200_OK)
