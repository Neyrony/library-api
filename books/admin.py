from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from books.models import Book


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ("title", "author", "cover", "inventory", "daily_fee")
    search_fields = (
        "title",
        "author",
    )
    list_filter = ("cover",)
    ordering = ("title",)
    list_per_page = 25
    fieldsets = ()
