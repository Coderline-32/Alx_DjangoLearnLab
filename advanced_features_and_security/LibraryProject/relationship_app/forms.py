# relationship_app/forms.py
from django import forms
from .models import Book, Author # Import Author if BookForm needs it for ForeignKey

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        # You might want to add widgets or labels here for better UI