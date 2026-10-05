from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
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
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f"{self.title} ({self.author})"

    class Meta:
        ordering = ["title"]
        constraints = [
            UniqueConstraint(
                fields=["title", "author", "cover"], name="unique_title_author_cover"
            ),
        ]
