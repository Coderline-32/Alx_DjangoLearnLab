from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and authenticate client
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # Create sample books
        self.book1 = Book.objects.create(title="Book One", author="Author A", publication_year=2000)
        self.book2 = Book.objects.create(title="Book Two", author="Author B", publication_year=2010)
        self.book3 = Book.objects.create(title="Another Book", author="Author A", publication_year=2005)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_books_by_author(self):
        url = reverse('book-list') + '?author=Author A'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # book1 and book3

    def test_search_books(self):
        url = reverse('book-list') + '?search=Another'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Another Book")

    def test_order_books_by_publication_year_desc(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_retrieve_book_detail(self):
        url = reverse('book-detail', args=[self.book1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated(self):
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'author': 'Author New',
            'publication_year': 2025
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(pk=response.data['id']).title, 'New Book')

    def test_create_book_unauthenticated(self):
        self.client.logout()
        url = reverse('book-create')
        data = {'title': 'Unauthorized Book', 'author': 'None', 'publication_year': 2025}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        url = reverse('book-update', args=[self.book1.pk])
        data = {'title': 'Updated Book Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')

    def test_update_book_unauthenticated(self):
        self.client.logout()
        url = reverse('book-update', args=[self.book1.pk])
        data = {'title': 'Fail Update'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        url = reverse('book-delete', args=[self.book1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_delete_book_unauthenticated(self):
        self.client.logout()
        url = reverse('book-delete', args=[self.book2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Book.objects.filter(pk=self.book2.pk).exists())
