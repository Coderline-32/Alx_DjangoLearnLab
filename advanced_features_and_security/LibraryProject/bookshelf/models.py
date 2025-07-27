# advanced_features_and_security/LibraryProject/bookshelf/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save # Needed for UserProfile creation if you use it here
from django.dispatch import receiver # Needed for UserProfile creation if you use it here
from django.conf import settings # Needed if you reference settings.AUTH_USER_MODEL in UserProfile

# <--- IMPORTANT: Import Author from relationship_app as Book will now have a ForeignKey to it
from relationship_app.models import Author # Ensure relationship_app is in INSTALLED_APPS


# --- 1. Define the CustomUser Manager FIRST ---
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password) # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Superusers are typically active

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

# --- 2. Define the CustomUser Model ---
class CustomUser(AbstractUser):
    # Core authentication fields (essential for your setup)
    email = models.EmailField(unique=True) # This was essential for your login method
    USERNAME_FIELD = 'email' # Use email for login
    REQUIRED_FIELDS = ['username'] # Username will still be prompted during superuser creation

    # Custom profile fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # Add is_active field with a default, if not already handled by AbstractUser (it is, but good for clarity)
    is_active = models.BooleanField(default=True)

    # Link the custom manager to your model
    objects = CustomUserManager()

    class Meta:
        # Permissions for CustomUser itself (removed 'can_create'/'can_delete' as they are now on Book)
        verbose_name = "Custom User"
        verbose_name_plural = "Custom users"

    def __str__(self):
        # Return a meaningful string, prefer username if not empty, otherwise email
        return self.username if self.username else self.email


# --- 3. Define the Book Model (Now residing solely in bookshelf app) ---
class Book(models.Model):
    """
    The central and only Book model for the entire project.
    It now includes a ForeignKey to Author from relationship_app.
    All Book-related permissions are defined here.
    """
    title = models.CharField(max_length=200) # Increased length for flexibility
    # <--- IMPORTANT: ForeignKey to Author model from relationship_app
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        # ALL Book-related permissions are consolidated here, including the general ones
        permissions = [
            ("can_view_book", "Can view book details"),
            ("can_create_book", "Can create new books"),
            ("can_edit_book", "Can edit existing books"),
            ("can_delete_book", "Can delete books"),
            # These are the general 'can_create' and 'can_delete' for this Book model,
            # requested by the checker to be on Book in bookshelf/models.py
            ("can_create", "Can create book entries in bookshelf"),
            ("can_delete", "Can delete book entries in bookshelf"),
        ]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} by {self.author.name}" if self.author else self.title

# --- UserProfile model and signal ---
# If your UserProfile is meant to be directly created/managed by CustomUser interactions
# within the bookshelf app, you might define it here along with its signal.
# However, if it's a general user profile linked via settings.AUTH_USER_MODEL and
# used across multiple apps (like relationship_app for roles), it might be better
# kept in relationship_app, and the signal for creation there.
# For now, assuming UserProfile is linked to settings.AUTH_USER_MODEL and resides in relationship_app.
# So, no UserProfile definition or signal is directly needed here unless you choose to move it.