from rest_framework import serializers

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
            "actual_return_date",
            "user",
            "book",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.StringRelatedField(read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")


class BorrowingRetrieveSerializer(BorrowingSerializer):
    user = UserSerializer(read_only=True)
    book = BookListRetrieveSerializer(read_only=True)
