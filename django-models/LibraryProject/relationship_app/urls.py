from django.urls import path
from . import views
from .views_ext.admin_view import admin_view
from .views_ext.librarian_view import librarian_view
from .views_ext.member_view import member_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from . import views



urlpatterns = [
    path('', views.home_view, name= 'home' ),
    path('books/', views.list_books, name= 'list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    path('register/', views.register, name='register'),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
    path('accounts/login/', auth_views.LoginView.as_view(), name= 'login'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]