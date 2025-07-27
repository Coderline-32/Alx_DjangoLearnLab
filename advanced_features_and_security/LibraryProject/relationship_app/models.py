# advanced_features_and_security/LibraryProject/relationship_app/models.py

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# <--- IMPORTANT: Add this import to reference the Book model in bookshelf app
from bookshelf.models import Book


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# --- REMOVED: The Book model class definition was here ---

class Library(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    # <--- IMPORTANT: This ManyToManyField now refers to the Book model in bookshelf.models
    books = models.ManyToManyField(Book, related_name='libraries')
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='Member')
    else:
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()