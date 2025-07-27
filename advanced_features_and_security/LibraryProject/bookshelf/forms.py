# advanced_features_and_security/LibraryProject/bookshelf/forms.py

from django import forms
from .models import Book # Book is now in bookshelf.models
from relationship_app.models import Author # Author is still in relationship_app

class BookForm(forms.ModelForm):
    author_name = forms.CharField(max_length=100, label="Author Name",
                                  help_text="Type the author's full name. If they don't exist, a new author will be created.")

    class Meta:
        model = Book
        fields = ['title', 'author_name', 'publication_year']

    def clean_author_name(self):
        author_name = self.cleaned_data['author_name']
        if not author_name:
            raise forms.ValidationError("Author name cannot be empty.")
        # Ensure correct handling of Author creation/retrieval
        author, created = Author.objects.get_or_create(name__iexact=author_name, defaults={'name': author_name.strip()})
        self.instance.author = author # Assign the author to the book instance
        return author_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.author:
            self.fields['author_name'].initial = self.instance.author.name