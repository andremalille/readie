"""
Django management command to create a superuser at deployment time.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    """Creates a superuser if none exists."""
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        self.stdout.write('Checking for superuser...')

        admin_username = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'adminpassword')

        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(self.style.SUCCESS(f'Superuser "{admin_username}" already exists'))
            return

        required_fields = []
        for field in User._meta.fields:
            if field.name != 'username' and field.name != 'password' and not field.blank and not field.null:
                required_fields.append(field.name)

        user_kwargs = {
            'username': admin_username,
            'email': admin_email,
        }

        for field in required_fields:
            if field not in user_kwargs and field != 'password':
                user_kwargs[field] = f'default_{field}'

        try:
            user = User.objects.create_superuser(
                **user_kwargs,
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{admin_username}"'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to create superuser: {str(e)}'))