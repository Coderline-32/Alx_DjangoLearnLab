from django.db import models


# Create your models here.

class Author(models.Model):
    """
    Represents an author of books.
    """
    name = models.CharField(max_length=100)

class Book(models.Model):
    """
    Represents a book written by an author.
    """
     
    title = models.CharField(max_length=100)
    publication_year = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, related_name='book', on_delete=models.CASCADE)

