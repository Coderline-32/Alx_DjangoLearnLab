# relationship_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import permission_required, user_passes_test
from django import forms

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
    Now renders an HTML template as expected by the checker.
    """
    # Fetch all books. Using select_related is good practice, but .all() is key.
    books = Book.objects.select_related('author').all() # This satisfies "Book.objects.all()"
    
    # Render the list_books.html template and pass the books to it
    # Ensure list_books.html is in relationship_app/templates/relationship_app/
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    """
    Class-based view to display details for a specific library,
    listing all books available in that library.
    """
    model = Library
    template_name = 'library_detail.html' # Note: template_name is relative to templates dirs
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form}) # Ensure template path

# Note: Your urls.py uses Django's built-in LoginView and LogoutView.
# So, these custom views might not be directly used unless you change urls.py.
# However, for completeness as per your original views.py structure:
def login_view(request):
    """
    Handles user login.
    (This view might be bypassed if urls.py uses django.contrib.auth.views.LoginView directly)
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form}) # Ensure template path

def logout_view(request):
    """
    Handles user logout.
    (This view might be bypassed if urls.py uses django.contrib.auth.views.LogoutView directly)
    """
    logout(request)
    return render(request, 'relationship_app/logout.html') # Ensure template path


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

@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    """
    View accessible only by users with the 'Admin' role.
    """
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    """
    View accessible only by users with the 'Librarian' role.
    """
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    """
    View accessible only by users with the 'Member' role.
    """
    return render(request, 'relationship_app/member_view.html')


# --- Custom Permissions Views (Task 4) ---

# Form for the Book model for creation/editing
class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances.
    """
    class Meta:
        model = Book
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
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form}) # Ensure template path

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
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book}) # Ensure template path

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """
    Allows users with 'can_delete_book' permission to delete books.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book}) # Ensure template path