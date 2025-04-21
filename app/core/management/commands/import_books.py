import csv
from django.core.management.base import BaseCommand
from core.models import Book


class Command(BaseCommand):
    help = 'Imports books from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        with open(options['csv_path'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                try:
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

                    Book.objects.create(
                        isbn13=row.get('isbn13', '')[:13],
                        isbn10=row.get('isbn10', '')[:10],
                        title=row.get('title', '')[:255],
                        subtitle=row.get('subtitle', '')[:255],
                        authors=row.get('authors', '')[:255],
                        categories=row.get('categories', '')[:255],
                        description=row.get('description', ''),
                        published_year=published_year,
                        average_rating=average_rating
                    )

                    if i % 100 == 0:
                        self.stdout.write(f"Processed {i} records...")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error importing row {i} ({row.get('title')}): {str(e)}"
                    ))
                    continue

        self.stdout.write(self.style.SUCCESS(
            f"Successfully imported books. Processed {i} records."
        ))