from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookListRetrieveSerializer(BookSerializer):
    cover = serializers.CharField(read_only=True, source="get_cover_display")
