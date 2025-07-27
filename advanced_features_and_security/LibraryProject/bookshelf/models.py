# advanced_features_and_security/LibraryProject/bookshelf/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save # Needed for UserProfile creation if you use it here
from django.dispatch import receiver # Needed for UserProfile creation if you use it here
from django.conf import settings # Needed if you reference settings.AUTH_USER_MODEL in UserProfile

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
        # Add the custom permissions the checker is looking for
        permissions = [
            ("can_create", "Can create records/entries"),
            ("can_delete", "Can delete records/entries"),
        ]
        # Optional: Add verbose names for better admin display
        verbose_name = "Custom User"
        verbose_name_plural = "Custom users"

    def __str__(self):
        # Return a meaningful string, prefer username if not empty, otherwise email
        return self.username if self.username else self.email


