# advanced_features_and_security/LibraryProject/bookshelf/urls.py

from django.urls import path
from . import views # Import views from the bookshelf app

app_name = 'bookshelf' # Define the app_name for URL namespacing (good practice)

urlpatterns = [
    # URL for the ExampleForm view
    # This assumes you'll create a view named 'example_form_view' in bookshelf/views.py
    path('example-form/', views.example_form_view, name='example_form'),

    # Add any other URLs specific to the 'bookshelf' app here if needed in the future
    # For example, user profiles if they were managed directly by bookshelf views:
    # path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
]