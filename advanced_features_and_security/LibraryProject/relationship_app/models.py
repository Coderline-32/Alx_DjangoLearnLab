from django.db import models
from django.conf import settings # <-- NEW: Import settings to reference AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver


# --- Custom User Model (Defined first as it's referenced by UserProfile) ---

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100) # Consistent with previous

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200) # Reverted to 200 from 100 for consistency
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name='books') # <-- ADDED related_name
    publication_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=200) # Reverted to 200 from 100 for consistency
    address = models.CharField(max_length=300) # Reverted to 300 from 255 for consistency
    books = models.ManyToManyField(Book, related_name='libraries') # <-- ADDED related_name
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    def __str__(self):
        return self.name

# --- FIXED UserProfile ---
class UserProfile(models.Model):
    # This was duplicated and pointing to the wrong User model.
    # It must point to the custom user model defined by AUTH_USER_MODEL in settings.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    # max_length=20 is fine, even if choices are shorter.
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# --- FIXED post_save receiver ---
# The sender must be your CustomUser model, not the default Django User model.
@receiver(post_save, sender=settings.AUTH_USER_MODEL) # Use settings.AUTH_USER_MODEL here as well
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='Member')
    else:
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()