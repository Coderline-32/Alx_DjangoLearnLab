from django.urls import path
# Import all views from the local views.py file
from . import views
# Import Django's built-in authentication views for direct use
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    # General views
    path('', views.home_view, name='home'),
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),

    # User Authentication views (Task 2)
    # Using Django's built-in views for login/logout directly for simplicity.
    # Ensure 'register_view' is correctly named in your views.py
    path('register/', views.register_view, name='register'), # Corrected to views.register_view
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Role-based access control views (Task 3)
    # Now accessed via 'views.' since they are in the main views.py
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),

    # Custom Permissions views for Book management (Task 4)
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]