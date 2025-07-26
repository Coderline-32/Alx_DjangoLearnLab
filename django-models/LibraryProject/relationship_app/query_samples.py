import os
import sys
import django

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

# Initialize Django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author.name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'")

def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in library '{library.name}':")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")

def get_librarian_of_library(library_name):
    try:
        librarian = Librarian.objects.get(library__name=library_name)
        print(f"Librarian of library '{library_name}': {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to library '{library_name}'")

if __name__ == "__main__":
    # Replace these names with actual data in your database
    author_name = "J.K. Rowling"
    library_name = "Central Library"

    query_books_by_author(author_name)
    print()
    list_books_in_library(library_name)
    print()
    get_librarian_of_library(library_name)
