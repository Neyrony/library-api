from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "borrowing",
        "status",
        "type",
        "money_to_pay",
        "created_at",
        "session_id",
        "session_url",
    )
    list_filter = (
        "status",
        "type",
    )
    search_fields = (
        "session_id",
        "borrowing__book__title",
    )
    ordering = ("-borrowing__expected_return_date",)
    list_per_page = 25
