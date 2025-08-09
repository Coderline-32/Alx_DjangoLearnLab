from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

class AuthorSerializer(serializers.ModelSerializer):

    books = BookSerializer(many=True, read_noly=True, source='books')
    class Meta:
        model = Author
        fields = ['name']
