import os
import tempfile

from PIL import Image
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


def create_user(email='user@example.com', password='testpass123', name='Test User'):
    """Create a new user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        name=name,
    )


class TestUser(TestCase):
    """Tests for user correct functionality"""
    def setUp(self):
        self.client = Client()
        self.user = create_user()

    def test_user_registration_get(self):
        """Test user registration GET method"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_user_registration_post(self):
        """Test user registration POST method"""
        response = self.client.post(reverse('register'), data={
            'email': 'new@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_user_registration_post_error(self):
        """Test user registration POST method with invalid data"""
        response = self.client.post(reverse('register'), data={
            'email': 'new@example.com',
            'password': 'newpass123',
            'confirm_password': 'wrongpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'confirm_password', 'Passwords do not match.')

    def test_user_login_get(self):
        """Test user login GET method"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_login_post(self):
        """Test user login POST method"""
        response = self.client.post(reverse('login'), data={
            'email': 'user@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_user_login_post_error(self):
        """Test user login POST method with invalid data"""
        response = self.client.post(reverse('login'), data={
            'email': 'user@example.com',
            'password': 'wrongpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password.')

    def test_user_logout(self):
        """Test user logout method"""
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_user_name_get(self):
        """Test username GET method"""
        response = self.client.get(reverse('name'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_name.html')

    def test_user_name_post(self):
        """Test username POST method"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('name'), data={
            'name': 'Test Name',
        })

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.name, 'Test Name')

    def test_user_profile_requires_login(self):
        """Test user profile requires login"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_logged_in(self):
        """Test if user is logged in to open profile"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_change_profile_image(self):
        """Test changing profile image"""
        self.client.force_login(self.user)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            response = self.client.post(reverse('change_profile_image'), {
                'image': image_file,
            }, follow=True)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.image.name.endswith('.jpg'))
        self.assertTrue(os.path.exists(self.user.image.path))

    def test_change_profile_image_get(self):
        """Test changing profile image if GET method occurs"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('change_profile_image'))
        self.assertEqual(response.status_code, 302)

    def test_change_info_get(self):
        """Test changing user info GET method"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('change_info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_profile.html')

    def test_change_info_name_post(self):
        """Test changing username and email POST method"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('change_info'), {
            'name': 'New Name',
            'email': 'newemail@example.com',
            'old_password': '',
            'new_password': '',
            'confirm_new_password': '',
        })

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.name, 'New Name')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_change_info_password_post(self):
        """Test changing user password POST method"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('change_info'), {
            'email': self.user.email,
            'name': self.user.name,
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'confirm_new_password': 'newpass123',
        })

        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.check_password('newpass123'))
        self.assertEqual(response.status_code, 302)

    def test_change_info_password_incorrect_old_post(self):
        """Test changing user password if the old one is incorrect POST method"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('change_info'), {
            'email': self.user.email,
            'name': self.user.name,
            'old_password': 'wrongtestpass123',
            'new_password': 'newpass123',
            'confirm_new_password': 'newpass123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your old password was entered incorrectly.')

    def test_change_info_password_incorrect_new_post(self):
        """Test changing user password if the passwords don't match POST method"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('change_info'), {
            'email': self.user.email,
            'name': self.user.name,
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'confirm_new_password': 'wrongnewpass123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New passwords don't match.")

    def test_change_info_password_empty_post(self):
        """Test changing user password if the old password wasn't provided POST method"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('change_info'), {
            'email': self.user.email,
            'name': self.user.name,
            'new_password': 'newpass123',
            'confirm_new_password': 'newpass123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter your old password to set a new one.")
