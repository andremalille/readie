"""
Django management command to create a superuser at deployment time.
"""
import os
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    """Creates a superuser if none exists."""
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        self.stdout.write('Checking for superuser...')

        available_fields = [field.name for field in User._meta.fields]
        self.stdout.write(f"Available User model fields: {', '.join(available_fields)}")

        username_field = getattr(User, 'USERNAME_FIELD', 'email')
        self.stdout.write(f"Using {username_field} as the username field")

        admin_identifier = os.environ.get(f'DJANGO_ADMIN_{username_field.upper()}',
                                         'admin@example.com' if username_field == 'email' else 'admin')
        admin_password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'adminpassword')

        self.stdout.write(f"Using {username_field}={admin_identifier}")

        filter_kwargs = {username_field: admin_identifier}
        try:
            if User.objects.filter(**filter_kwargs).exists():
                self.stdout.write(self.style.SUCCESS(
                    f'Superuser with {username_field}="{admin_identifier}" already exists'
                ))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error checking existing users: {str(e)}'))
            self.stdout.write(self.style.WARNING('Continuing with superuser creation attempt'))

        user_kwargs = {username_field: admin_identifier}

        for field in User._meta.fields:
            if field.name not in [username_field, 'password', 'id'] and not field.blank and not field.null:
                if field.name == 'name':
                    user_kwargs['name'] = os.environ.get('DJANGO_ADMIN_NAME', 'Admin User')
                elif field.name not in user_kwargs:
                    user_kwargs[field.name] = f'default_{field.name}'

        self.stdout.write(f"Creating superuser with kwargs: {user_kwargs}")

        try:
            user = User.objects.create_superuser(
                **user_kwargs,
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created superuser with {username_field}="{admin_identifier}"'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to create superuser: {str(e)}'))

            self.stdout.write(self.style.ERROR(f'Exception type: {type(e).__name__}'))
            self.stdout.write(self.style.ERROR(f'Exception args: {e.args}'))
            raise
