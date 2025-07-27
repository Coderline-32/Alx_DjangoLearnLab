from django.shortcuts import render
from .forms import ExampleForm
# Create your views here.


# advanced_features_and_security/LibraryProject/bookshelf/views.py

from django.shortcuts import render, redirect
from .forms import ExampleForm # Make sure this import is there

# ... (other imports or views you might have in bookshelf/views.py) ...

def example_form_view(request):
    """
    View to handle and display the ExampleForm.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the cleaned data here
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            print(f"ExampleForm Submission: Name={name}, Email={email}, Message={message}")
            # Redirect to a success page or another view
            return redirect('bookshelf:example_form') # Redirect back to itself for simplicity, or a success page
    else:
        form = ExampleForm() # An empty form for GET requests

    return render(request, 'bookshelf/form_example.html', {'form': form})