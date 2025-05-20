import csv
import traceback
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Book


class Command(BaseCommand):
    """Import books from csv file with smart duplicate detection."""
    help = 'Imports books from CSV, skipping duplicates'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)
        parser.add_argument('--batch-size', type=int, default=100,
                            help='Number of records to process in a batch')
        parser.add_argument('--force', action='store_true',
                            help='Force import of all records, updating existing ones')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        batch_size = options['batch_size']
        force_update = options['force']

        self.stdout.write(f"Starting import from {csv_path}")
        total_records = 0
        new_count = 0
        skip_count = 0
        update_count = 0
        error_count = 0
        error_details = []

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                total_records = sum(1 for _ in csv.DictReader(f))

            self.stdout.write(f"Found {total_records} records in CSV file")

            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, 1):
                    try:
                        isbn13 = row.get('isbn13', '')[:13]
                        isbn10 = row.get('isbn10', '')[:10]
                        title = row.get('title', '')[:255]

                        existing_book = None
                        if isbn13:
                            existing_book = Book.objects.filter(isbn13=isbn13).first()
                        if not existing_book and isbn10:
                            existing_book = Book.objects.filter(isbn10=isbn10).first()
                        if not existing_book and title:
                            existing_book = Book.objects.filter(title=title).first()

                        published_year = None
                        if row.get('published_year'):
                            try:
                                published_year = int(float(row['published_year']))
                            except (ValueError, TypeError):
                                pass

                        average_rating = 0.0
                        if row.get('average_rating'):
                            try:
                                rating = float(row['average_rating'])
                                average_rating = max(0.0, min(5.0, rating))
                            except (ValueError, TypeError):
                                pass

                        num_pages = None
                        if row.get('num_pages'):
                            try:
                                num_pages = int(float(row['num_pages']))
                            except (ValueError, TypeError):
                                pass

                        book_data = {
                            'isbn13': isbn13,
                            'isbn10': isbn10,
                            'title': title,
                            'subtitle': row.get('subtitle', '')[:255],
                            'authors': row.get('authors', '')[:255],
                            'categories': row.get('categories', '')[:255],
                            'description': row.get('description', ''),
                            'published_year': published_year,
                            'average_rating': average_rating,
                            'thumbnail': row.get('thumbnail', '')[:255],
                            'num_pages': num_pages,
                        }

                        with transaction.atomic():
                            if existing_book:
                                if force_update:
                                    for key, value in book_data.items():
                                        setattr(existing_book, key, value)
                                    existing_book.save()
                                    update_count += 1
                                else:
                                    skip_count += 1
                            else:
                                Book.objects.create(**book_data)
                                new_count += 1

                        if i % batch_size == 0:
                            self.stdout.write(
                                f"Processed {i}/{total_records} records... "
                                f"(New: {new_count}, Updated: {update_count}, Skipped: {skip_count}, Errors: {error_count})"
                            )

                    except Exception as e:
                        error_count += 1
                        error_msg = f"Row {i} ({row.get('title', 'Unknown')}): {str(e)}"
                        error_details.append(error_msg)
                        self.stdout.write(self.style.ERROR(error_msg))

                        self.stdout.write(self.style.ERROR(traceback.format_exc()))
                        continue

            self.stdout.write(self.style.SUCCESS(
                f"Import completed: {new_count} new books, {update_count} updated, "
                f"{skip_count} skipped, {error_count} errors (out of {total_records} total)"
            ))

            if new_count + update_count + skip_count + error_count < total_records:
                self.stdout.write(self.style.WARNING(
                    f"Warning: {total_records - (new_count + update_count + skip_count + error_count)} books were not processed"
                ))

            if error_count > 0:
                self.stdout.write(self.style.WARNING(
                    f"First 10 error details (total {error_count}):"
                ))
                for error in error_details[:10]:
                    self.stdout.write(f"  - {error}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Fatal error processing CSV: {str(e)}"))
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
