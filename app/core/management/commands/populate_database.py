"""
Django management command to populate the database at deployment time.
"""
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from core.models import Book


class Command(BaseCommand):
    """Populate the database with initial data."""
    help = 'Populates the database with initial data including books'

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')

        if Book.objects.exists():
            self.stdout.write(self.style.WARNING(
                'Books already exist in the database. Skipping import to avoid duplicates.'
            ))
            self.stdout.write(f'Current book count: {Book.objects.count()}')
            return

        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data',
                                'books.csv')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at: {csv_path}'))

            alternatives = [
                '/app/books.csv',
                '/app/data/books.csv',
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'books.csv')
            ]

            for alt_path in alternatives:
                if os.path.exists(alt_path):
                    self.stdout.write(self.style.SUCCESS(f'Found CSV at alternative location: {alt_path}'))
                    csv_path = alt_path
                    break
            else:
                self.stdout.write(self.style.ERROR('Could not find books.csv in any location'))
                return

        self.stdout.write(f'Importing books from {csv_path}...')
        try:
            call_command('import_books', csv_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully imported books. Total count: {Book.objects.count()}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing books: {str(e)}'))