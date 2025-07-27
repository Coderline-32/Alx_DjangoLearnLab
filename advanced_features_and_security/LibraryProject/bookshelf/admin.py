from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these columns in the list view
    search_fields = ('title', 'author')                     # Enable search by title or author
    list_filter = ('publication_year',)                     # Add filter by year

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Info (Custom)', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal Info (Custom)', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = UserAdmin.list_display + ('date_of_birth',)
try:
    from django.contrib.auth.models import User
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass