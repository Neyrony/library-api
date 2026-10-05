from django.urls import path, include
from rest_framework import routers

from books.views import BookViewSet

books_router = routers.DefaultRouter()
books_router.register("", BookViewSet, basename="book")

urlpatterns = [path("", include(books_router.urls))]

app_name = "books"
