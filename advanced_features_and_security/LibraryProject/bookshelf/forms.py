# advanced_features_and_security/LibraryProject/bookshelf/forms.py

from django import forms

class ExampleForm(forms.Form):
    """
    A simple example form as required by the checker.
    This form can be used for demonstration or testing purposes.
    """
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")