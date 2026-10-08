from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint, F
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD", _("Hard")
        SOFT = "SOFT", _("Soft")

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=16,
        choices=CoverChoices.choices,
        default=CoverChoices.HARD,
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f"{self.title} ({self.author})"

    def increase_inventory(self):
        Book.objects.filter(id=self.id).update(inventory=F("inventory") + 1)

    def decrease_inventory(self):
        update = Book.objects.filter(id=self.id, inventory__gt=0).update(
            inventory=F("inventory") - 1
        )

        if update:
            return True
        return False

    class Meta:
        ordering = ["title"]
        constraints = [
            UniqueConstraint(
                fields=["title", "author", "cover"], name="unique_title_author_cover"
            ),
        ]
