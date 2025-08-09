# api/views.py
from rest_framework import generics, permissions, filters
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import BookSerializer
from django_filters import rest_framework 
from django_filters.rest_framework import DjangoFilterBackend
# List all books (open to everyone)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Add filtering, searching, ordering backends
    filter_backends = [
        DjangoFilterBackend,   # for filtering by exact fields
        filters.SearchFilter,  # for text search
        filters.OrderingFilter # for ordering results
    ]

    # Fields available for filtering by exact match or range (can customize)
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields available for search (text-based)
    search_fields = ['title', 'author']

    # Fields available for ordering results
    ordering_fields = ['title', 'publication_year']

    # Optional: default ordering if none specified
    ordering = ['title']





# Retrieve single book by ID (open to everyone)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Create a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Optional: You can add custom logic here, e.g., associate with user
        serializer.save()

# Update existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Delete a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
