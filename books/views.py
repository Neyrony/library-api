from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from books.permissions import IsAdminOrReadOnly
from books.serializers import BookSerializer, BookListRetrieveSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Show a list of book",
        description="Show a list of all books with pagination",
    ),
    retrieve=extend_schema(
        summary="Show a particular book",
        description="Show detailed information about a particular book",
    ),
    create=extend_schema(
        summary="Create a new book",
    ),
    update=extend_schema(
        summary="Update a book",
    ),
    partial_update=extend_schema(
        summary="Partially update a book",
    ),
    destroy=extend_schema(
        summary="Delete a book",
    ),
)
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookListRetrieveSerializer
        return BookSerializer
