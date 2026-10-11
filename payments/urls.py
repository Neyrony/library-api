from django.urls import path, include
from rest_framework import routers

from payments.views import PaymentViewSet

payments_router = routers.DefaultRouter()

payments_router.register("", PaymentViewSet, basename="payment")

urlpatterns = [path("", include(payments_router.urls))]

app_name = "payments"
