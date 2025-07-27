# bookshelf/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager # Keep AbstractUser for CustomUser

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        """
        Returns a string representation of the Book instance.
        This is useful for display in the Django admin and shell.
        """
        return f"{self.title} by {self.author} ({self.publication_year})"
    

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

