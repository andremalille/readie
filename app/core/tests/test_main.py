from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestMain(TestCase):
    """Test for main page loading"""
    def test_load_main_page(self):
        """Test loading main page"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')
