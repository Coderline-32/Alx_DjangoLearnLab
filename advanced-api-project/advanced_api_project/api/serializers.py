from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    
    """
    Serializes all fields of the Book model.
    Adds custom validation to ensure the publication_date is not in the future.
    """
    class Meta:
        model = Book
        fields = '__all__'
    def validate_publication_date(self, value):
        """
        Custom validation for the publication_date field.
        Ensures the publication date is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError('Publication date cannot be current date')
        return value
    
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model, including the 'name' field
    and a nested serialization of related books using BookSerializer.
    """

    books = BookSerializer(many=True, read_only=True, source='books')
    class Meta:
        model = Author
        fields = ['name', 'books']
