# advanced_features_and_security/LibraryProject/relationship_app/urls.py

from django.urls import path
from . import views # Import views from the current app
# from django.contrib.auth.views import LoginView, LogoutView # REMOVED: LoginView/LogoutView are now in bookshelf app's views

urlpatterns = [
    

    # --- KEEP: Library-specific views (as Library model is still in relationship_app) ---
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),

    # --- KEEP: Role-based access control views (assuming these are specific to relationship_app's UserProfile roles) ---
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]