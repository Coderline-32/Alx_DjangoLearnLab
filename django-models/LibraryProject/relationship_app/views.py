Got it\! Here's the consolidated `relationship_app/views.py` file, incorporating all your existing logic, the role-based views (from your `views_ext` directory) directly into this file, and the placeholder views for Task 4 (add, edit, delete book) with their respective permission decorators and forms.

**Make sure you have created the `BookForm` in the same `views.py` or imported it if it's in another file (I've included it directly here for completeness).**

```python
# relationship_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import permission_required, user_passes_test # Make sure user_passes_test is imported
from django import forms # Import forms for custom permission views

# Import your models
from .models import Author, Book, Library, Librarian, UserProfile


# --- Basic Views ---
def home_view(request):
    """
    A simple home view for the application.
    """
    return HttpResponse("Welcome to the Library app!")

def list_books(request):
    """
    Function-based view to list all books and their authors.
    Renders a plain text list.
    """
    books = Book.objects.select_related('author').all() # Efficiently fetch related authors
    lines = [f"{book.title} by {book.author.name}" for book in books]
    response_text = "\n".join(lines)
    return HttpResponse(response_text, content_type="text/plain")

class LibraryDetailView(DetailView):
    """
    Class-based view to display details for a specific library,
    listing all books available in that library.
    """
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure 'books' context variable is populated correctly for the template
        context['books'] = self.object.books.all()
        return context


# --- User Authentication Views ---
def register_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books') # Redirect to a suitable page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # You might want to add a 'next' parameter for redirecting to the page
            # the user was trying to access before being logged out/in.
            return redirect('list_books') # Redirect to a suitable page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    return render(request, 'logout.html')


# --- Role-Based Access Control Views (Task 3) ---

# Helper functions for role checking
def is_admin(user):
    """Checks if the user has an 'Admin' role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Checks if the user has a 'Librarian' role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Checks if the user has a 'Member' role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin, login_url='/login/') # Redirect to login if not an admin
def admin_view(request):
    """
    View accessible only by users with the 'Admin' role.
    """
    # Ensure the template path matches your template directory structure
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian, login_url='/login/') # Redirect to login if not a librarian
def librarian_view(request):
    """
    View accessible only by users with the 'Librarian' role.
    """
    # Ensure the template path matches your template directory structure
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member, login_url='/login/') # Redirect to login if not a member
def member_view(request):
    """
    View accessible only by users with the 'Member' role.
    """
    # Ensure the template path matches your template directory structure
    return render(request, 'relationship_app/member_view.html')


# --- Custom Permissions Views (Task 4) ---

# Form for the Book model for creation/editing
class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances.
    """
    class Meta:
        model = Book
        # Ensure these fields match your Book model fields that you want to expose in the form
        fields = ['title', 'author'] # Add 'publication_year' if you added it to the model

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    Allows users with 'can_add_book' permission to add new books.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a relevant page after successful addition, e.g., the book list
            return redirect('list_books')
    else:
        form = BookForm()
    # Ensure this template exists in your templates directory
    return render(request, 'add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """
    Allows users with 'can_change_book' permission to edit existing books.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            # Redirect to a relevant page after successful update
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    # Ensure this template exists in your templates directory
    return render(request, 'edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """
    Allows users with 'can_delete_book' permission to delete books.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        # Redirect to a relevant page after successful deletion
        return redirect('list_books')
    # Ensure this template exists in your templates directory
    return render(request, 'delete_book.html', {'book': book})

```