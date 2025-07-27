

This is a summary of all 4 actions in one file:

```markdown
# CRUD Operations Summary for Book Model

## ✅ Create

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
