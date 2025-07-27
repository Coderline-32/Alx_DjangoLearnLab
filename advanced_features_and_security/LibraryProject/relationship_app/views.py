from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from relationship_app.models import Author, Book, Library, Librarian, UserProfile
from bookshelf.forms import ExampleForm
from bookshelf.models import CustomUser
from django import forms
from .models import Library
from LibraryProject.bookshelf.forms import BookForm

# Import all necessary models
from .models import Author, Book, Library, Librarian, UserProfile


# --- Basic Views ---
def home_view(request):
    """
    A simple home view for the application.
    """
    return HttpResponse("Welcome to the Library app!")



class LibraryDetailView(DetailView):
    """
    Class-based view to display details for a specific library,
    listing all books available in that library.
    Uses explicit template path 'relationship_app/library_detail.html'.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html' # Explicitly specified for checker
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # This fetches books related to the specific library instance
        context['books'] = self.object.books.all()
        return context


# --- User Authentication Views ---
def register_view(request):
    """
    Handles user registration.
    Renders 'relationship_app/register.html'.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books') # Redirect to a suitable page after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# --- Role-Based Access Control Views (Task 3) ---

# Helper functions for role checking
def is_admin(user):
    """Checks if the user has an 'Admin' role based on UserProfile."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Checks if the user has a 'Librarian' role based on UserProfile."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Checks if the user has a 'Member' role based on UserProfile."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin, login_url='/login/') # Redirect to login if not an admin
def admin_view(request):
    """
    View accessible only by users with the 'Admin' role.
    Renders 'relationship_app/admin_view.html'.
    """
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian, login_url='/login/') # Redirect to login if not a librarian
def librarian_view(request):
    """
    View accessible only by users with the 'Librarian' role.
    Renders 'relationship_app/librarian_view.html'.
    """
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member, login_url='/login/') # Redirect to login if not a member
def member_view(request):
    """
    View accessible only by users with the 'Member' role.
    Renders 'relationship_app/member_view.html'.
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
        # Ensure these fields match your Book model fields that you want to expose in the form
        fields = ['title', 'author'] # Add 'publication_year' if you added it to the model

