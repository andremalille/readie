import json
from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create a new user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
    )


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


class TestBooks(TestCase):
    """Tests for books correct functionality"""
    def setUp(self):
        self.client = Client()
        self.user = create_user()
        self.book1 = create_book()
        self.book2 = create_book(
            isbn13='1234567890321',
            isbn10='1234567897',
            title='Test Two',
            authors='Test Author 3',
            categories='Test Category 3',
            published_year=2015,
            average_rating=Decimal('5.00'),
            thumbnail='exampletest.com',
            num_pages=700,
        )
        self.book_list = models.BookList.objects.create(
            user=self.user,
            book=self.book1,
            status='currently_reading',
            favourites=False,
            pages_read=50,
        )

    def test_books_requires_login(self):
        """Test that a user has to be authenticated"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_display_books(self):
        """Test the display books page"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('books'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertContains(response, 'Test Book')
        self.assertContains(response, 'Test Two')

    def test_book_search(self):
        """Test the search for a book"""
        self.client.force_login(self.user)
        response = self.client.get(
            f"{reverse('books')}?action=search&q=Book"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertNotContains(response, 'Test Two')

    def test_book_filter_by_category(self):
        """Test the filtering of a book by category"""
        self.client.force_login(self.user)
        response = self.client.get(
            f"{reverse('books')}?action=filter&categories=Test+Category+1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertNotContains(response, 'Test Two')

    def test_book_filter_by_pages(self):
        """Test the filtering of a book by pages"""
        self.client.force_login(self.user)
        response = self.client.get(
            f"{reverse('books')}?action=filter&pages_min=250&pages_max=350"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertNotContains(response, 'Test Two')

    def test_book_filter_by_rating(self):
        """Test the filtering of a book by rating"""
        self.client.force_login(self.user)
        response = self.client.get(
            f"{reverse('books')}?action=filter&rating_min=2.00&rating_max=4.50"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertNotContains(response, 'Test Two')

    def test_book_filter_by_year(self):
        """Test the filtering of a book by year"""
        self.client.force_login(self.user)
        response = self.client.get(
            f"{reverse('books')}?action=filter&year_min=1990&year_max=2010"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertNotContains(response, 'Test Two')

    def test_book_recommend(self):
        """Test the recommendation of a book"""
        self.client.force_login(self.user)
        models.BookList.objects.create(
            user=self.user,
            book=self.book2,
            status='finished',
            favourites=True,
        )
        book = create_book(
            title='Recommend Book',
            categories='Test Category 3',
        )

        response = self.client.get(
            f"{reverse('books')}?action=recommend"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recommend Book')

    def test_book_info(self):
        """Test displaying a book information"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('book_info', args=[self.book1.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertTemplateUsed(response, 'book_info.html')

    def test_book_add_to_list(self):
        """Test adding a book to a list"""
        self.client.force_login(self.user)
        number_of_books = models.BookList.objects.filter(user=self.user).count()
        response = self.client.post(
            reverse('add_book', args=[self.book2.pk]),
            {
                'status': 'read_later',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            models.BookList.objects.filter(user=self.user).count(),
            number_of_books + 1
        )
        self.assertTrue(
            models.BookList.objects.filter(
                user=self.user,
                book=self.book2,
            ).exists()
        )

    def test_display_user_list(self):
        """Test displaying a user list"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('user_list.html')
        self.assertContains(response, 'Test Book')
        self.assertNotContains(response, 'Test Two')

    def test_filter_by_categories_user_list(self):
        """Test the filtering of a user list by chosen categories"""
        self.client.force_login(self.user)
        models.BookList.objects.create(
            user=self.user,
            book=self.book2,
            status='finished',
            favourites=True,
        )
        response = self.client.get(
            f"{reverse('user_list')}?action=filter&statuses=currently_reading"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertNotContains(response, 'Test Two')

    def test_filter_by_favourites_user_list(self):
        """Test the filtering of a user list by favourites"""
        self.client.force_login(self.user)
        self.book_list.favourites = True
        self.book_list.save()
        models.BookList.objects.create(
            user=self.user,
            book=self.book2,
            status='finished',
            favourites=False,
        )
        response = self.client.get(
            f"{reverse('user_list')}?favourites=true"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertNotContains(response, 'Test Two')

    def test_display_user_book_info(self):
        """Test displaying a user book information"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_book_info', args=[self.book_list.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertTemplateUsed('user_book_info.html')

    def test_edit_book_get(self):
        """Test edit book GET method"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_book', args=[self.book_list.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertTemplateUsed('user_book_info.html')

    def test_edit_book_toggle_favourites(self):
        """Test edit book toggle favourites"""
        self.client.force_login(self.user)

        initial_value = self.book_list.favourites

        response = self.client.post(
            reverse('edit_book', args=[self.book_list.pk]),
            {'action_type': 'toggle_favourite'}
        )

        self.book_list.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book_list.favourites, not initial_value)

    def test_edit_book_change_status(self):
        """Test edit book change status"""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('edit_book', args=[self.book_list.pk]),
            {'action_type': 'change_status', 'status': 'finished'}
        )

        self.book_list.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book_list.status, 'finished')

    def test_edit_book_change_pages(self):
        """Test edit book change pages read"""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('edit_book', args=[self.book_list.pk]),
            {'action_type': 'change_pages', 'pages_read': '100'}
        )

        self.book_list.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book_list.pages_read, 100)

    def test_edit_book_change_status_ajax(self):
        """Test edit book change status via ajax"""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('edit_book', args=[self.book_list.pk]),
            {'action_type': 'change_status', 'status': 'finished'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.book_list.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['status_display'], 'Finished')
        self.assertEqual(self.book_list.status, 'finished')

    def test_edit_book_change_pages_ajax(self):
        """Test edit book change pages via ajax"""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('edit_book', args=[self.book_list.pk]),
            {'action_type': 'change_pages', 'pages_read': '100'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.book_list.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['pages_read'], 100)
        self.assertEqual(self.book_list.pages_read, 100)

    def test_delete_book(self):
        """Test deleting a book"""
        self.client.force_login(self.user)
        number_of_books = models.BookList.objects.filter(user=self.user).count()

        response = self.client.post(
            reverse('delete_book', args=[self.book_list.pk]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            models.BookList.objects.filter(user=self.user).count(), number_of_books - 1
        )
        self.assertFalse(
            models.BookList.objects.filter(
                pk=self.book_list.pk,
                user=self.user,
            ).exists()
        )

    def test_toggle_favourite(self):
        """Test toggling favourites"""
        self.client.force_login(self.user)

        initial_value = self.book_list.favourites

        response = self.client.post(
            reverse('toggle_favourite', args=[self.book_list.pk]),
        )

        self.book_list.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book_list.favourites, not initial_value)

    def test_toggle_favourites_ajax(self):
        """Test toggling favourites via ajax"""
        self.client.force_login(self.user)

        initial_value = self.book_list.favourites

        response = self.client.post(
            reverse('toggle_favourite', args=[self.book_list.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.book_list.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['is_favourite'], not initial_value)
        self.assertEqual(self.book_list.favourites, not initial_value)

    def test_edit_book_change_pages_error(self):
        """Test catching an error while changing pages read"""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('edit_book', args=[self.book_list.pk]),
            {'action_type': 'change_pages', 'pages_read': '700'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('errors', data)
