from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.serializers import BookListRetrieveSerializer
from borrowings.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "user",
            "book",
        )
        read_only_fields = ("id", "user")

    def validate_book(self, instance):
        if instance.inventory == 0:
            raise ValidationError(
                f"There are no {instance.title} available for borrowing."
            )

        return instance

    @transaction.atomic
    def create(self, validated_data):
        updated = validated_data["book"].decrease_inventory()

        if not updated:
            raise ValidationError("There are no books available for borrowing.")

        return super().create(validated_data)


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.StringRelatedField(read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
        )


class BorrowingRetrieveSerializer(BorrowingSerializer):
    user = UserSerializer(read_only=True)
    book = BookListRetrieveSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
        )
