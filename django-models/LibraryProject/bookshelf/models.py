# bookshelf/models.py

from django.db import models

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