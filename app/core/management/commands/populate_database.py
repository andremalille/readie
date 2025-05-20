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

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true',
                           help='Force update existing entries')

    def handle(self, *args, **options):
        force = options.get('force', False)
        self.stdout.write('Starting database population...')

        # Check if books already exist
        existing_count = Book.objects.count()
        if existing_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f'Found {existing_count} existing books in the database.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                'No books found in the database. Will perform full import.'
            ))

        # Find the CSV file
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data',
                                'books.csv')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'CSV file not found at: {csv_path}'))

            # Try alternative locations
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
            # Use our smart import_books command with skip detection
            import_args = [csv_path]
            if force:
                import_args.append('--force')

            call_command('import_books', *import_args)

            # Verify the results
            new_count = Book.objects.count()
            if new_count > existing_count:
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully imported {new_count - existing_count} new books. '
                    f'Total book count: {new_count}'
                ))
            elif new_count == existing_count and existing_count > 0:
                self.stdout.write(self.style.SUCCESS(
                    f'No new books were imported. Database already contains {existing_count} books.'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Book count did not increase as expected. Current count: {new_count}'
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing books: {str(e)}'))