from django.urls import path, include
from rest_framework import routers

from borrowings.views import BorrowingsViewSet

borrowings_router = routers.DefaultRouter()

borrowings_router.register("", BorrowingsViewSet, basename="borrowing")

urlpatterns = [path("", include(borrowings_router.urls))]

app_name = "borrowings"
