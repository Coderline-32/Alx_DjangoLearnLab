from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these columns in the list view
    search_fields = ('title', 'author')                     # Enable search by title or author
    list_filter = ('publication_year',)                     # Add filter by year
