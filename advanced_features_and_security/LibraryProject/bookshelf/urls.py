# advanced_features_and_security/LibraryProject/bookshelf/urls.py

from django.urls import path
from . import views # Import views from the bookshelf app

app_name = 'bookshelf' # Define the app_name for URL namespacing (good practice)

urlpatterns = [
    # --- Authentication URLs ---
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'), # Your main home page for the bookshelf app

    # --- Book Management URLs (MOVED HERE) ---
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]