"""
Tests for models
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='example.com', password='testpass123'):
    """Creates a new user"""
    return get_user_model().objects.create_user(email, password)


def create_book(**params):
    """Creates a new book"""
    defaults = {
        'isbn13': '1234567890123',
        'isbn10': '1234567890',
        'title': 'Test Book',
        'subtitle': 'Test Sub Book',
        'authors': 'Test Author 1, Test Author 2',
        'categories': 'Test Category 1, Test Category 2',
        'description': 'Sample Description.',
        'published_year': 2000,
        'average_rating': Decimal('3.75'),
        'thumbnail': 'example.com',
        'num_pages': 300,
    }
    defaults.update(params)
    return models.Book.objects.create(**defaults)


class ModelTests(TestCase):
    """Tests models"""
    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['test2@Example.com', 'test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating a new user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_book(self):
        """Test creating a book"""
        book = models.Book.objects.create(
            isbn13='1234567890123',
            isbn10='1234567890',
            title='Test Book',
            subtitle='Test Sub Book',
            authors='Test Author 1, Test Author 2',
            categories='Test Category 1, Test Category 2',
            description='Sample Description.',
            published_year=2000,
            average_rating=Decimal('3.75'),
            thumbnail='example.com',
            num_pages=300,
        )

        self.assertEqual(str(book), book.title)

    def test_create_book_list(self):
        """Test creating a book list"""
        user = create_user()
        book = create_book()

        book_list = models.BookList.objects.create(
            user=user,
            book=book,
            status='read_later',
            favourites=False,
            pages_read=0,
        )

        self.assertEqual(str(book_list), f"{book_list.book} | {book_list.user}")

    @patch('core.models.uuid.uuid4')
    def test_user_file_name_uuid(self, mock_uuid):
        """Test generating image patch"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/users/{uuid}.jpg')
