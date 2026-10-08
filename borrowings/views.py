from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingSerializer,
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
        queryset = Borrowing.objects.all()

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("user", "book")

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

                if user_id:
                    user_id_list = self._str_to_list_int(user_id)

                    queryset = queryset.filter(user_id__in=user_id_list)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
