import uuid
import os

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


def user_image_file_path(instance, filename):
    """Generate file path for new user image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'users', filename)


class UserManager(BaseUserManager):
    """Manager for users"""
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True, upload_to=user_image_file_path)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Book(models.Model):
    """Book model"""
    isbn13 = models.CharField(max_length=13)
    isbn10 = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    authors = models.CharField(max_length=255, blank=True)
    categories = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    thumbnail = models.CharField(max_length=255, blank=True)
    num_pages = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class BookList(models.Model):
    """List of books"""
    STATUS_CHOICES = [
        ('read_later', 'Read later'),
        ('currently_reading', 'Currently reading'),
        ('finished', 'Finished'),
        ('on_hold', 'On hold'),
        ('re_reading', 'Re-reading'),
        ('dropped_reading', 'Dropped reading'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    favourites = models.BooleanField(default=False)
    pages_read = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.book} | {self.user}"
