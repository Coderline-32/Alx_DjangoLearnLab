from django.urls import path
from .views import home_view, list_books, register_view, login_view, logout_view, LibraryDetailView
from .views_ext.admin_view import admin_view
from .views_ext.librarian_view import librarian_view
from .views_ext.member_view import member_view
from django.contrib.auth import views as auth_views
from .views import add_book, edit_book, delete_book




urlpatterns = [
    path('', home_view, name= 'home' ),
    path('books/', list_books, name= 'list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
    path('accounts/login/', auth_views.LoginView.as_view(), name= 'login'),
    path('books/add/', add_book, name='add_book'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
]