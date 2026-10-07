from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from borrowings.validation import validate_dates, validate_user_and_book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="borrowings"
    )

    def __str__(self):
        return f"{self.book.title} ({self.borrow_date})"

    def clean(self):
        if self.id:
            old_instance = Borrowing.objects.get(pk=self.id)
        else:
            old_instance = None

        validate_dates(self, old_instance, ValidationError)
        validate_user_and_book(self, old_instance, ValidationError)
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["borrow_date"]
