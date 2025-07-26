from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book

# Create your views here.
def home_view(request):
    return HttpResponse("Welcome to the Library app!")

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

@permission_required('relationship_app.can_add_book')
def add_book(request):
    # Implementation for adding a book (form handling)
    pass

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    # Implementation for editing a book by pk
    pass

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    # Implementation for deleting a book by pk
    pass