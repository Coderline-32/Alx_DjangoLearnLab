from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager # Keep AbstractUser for CustomUser
from django.conf import settings # <-- NEW: Import settings to reference AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver


# --- Custom User Model (Defined first as it's referenced by UserProfile) ---
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True) # User's specified upload_to

    def __str__(self):
        return self.username

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The email fields must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password) #Hash the password
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)  


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