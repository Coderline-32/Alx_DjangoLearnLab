# advanced_features_and_security/LibraryProject/relationship_app/forms.py

from django import forms
# from bookshelf.models import Book # <--- REMOVE THIS IMPORT (no longer needed here)
from .models import Author, Library, Librarian, UserProfile # Keep other imports if needed for other forms

# <--- REMOVE BookForm ENTIRELY FROM HERE ---
# class BookForm(forms.ModelForm):
#     # ... (removed) ...