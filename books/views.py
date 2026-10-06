from rest_framework.viewsets import ModelViewSet

from books.models import Book
from books.serializers import BookSerializer, BookListRetrieveSerializer
from permissions import IsAdminOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookListRetrieveSerializer
        return BookSerializer
