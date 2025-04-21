from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


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

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

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
    published_year = models.IntegerField(blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.title


class BookList(models.Model):
    """List of books"""
    CATEGORY_CHOICES = [
        ('read_later', 'Read later'),
        ('currently_reading', 'Currently reading'),
        ('finished', 'Finished'),
        ('favourites', 'Favourites'),
        ('dropped_reading', 'Dropped reading'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
