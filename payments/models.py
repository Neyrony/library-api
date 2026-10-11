from django.db import models
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")

    class TypeChoices(models.TextChoices):
        PAYMENT = "PAYMENT", _("Payment")
        FINE = "FINE", _("Fine")

    status = models.CharField(
        max_length=16, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    type = models.CharField(max_length=16, choices=TypeChoices.choices)
    borrowing = models.ForeignKey(
        "borrowings.Borrowing",
        on_delete=models.PROTECT,
        related_name="payments",
    )
    session_url = models.URLField(unique=True)
    session_id = models.CharField(max_length=255, unique=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{str(self.borrowing)} - {self.get_status_display()}"

    class Meta:
        ordering = ["borrowing__expected_return_date"]
