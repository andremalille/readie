#!/bin/sh
set -e

# Function for better error handling
handle_error() {
    echo "ERROR: Command failed with exit code $?: $1"
    exit 1
}

echo "========== Starting application deployment =========="

echo "Waiting for database..."
python manage.py wait_for_db || handle_error "Database connection failed"
echo "Database is available!"

echo "Creating a superuser..."
python manage.py ensure_superuser || handle_error "Failed to ensure superuser"
echo "Superuser check completed"

echo "Applying database migrations..."
python manage.py migrate || handle_error "Database migration failed"
echo "Migrations applied successfully"

echo "Checking current book count..."
python -c "from core.models import Book; print(f'Current book count: {Book.objects.count()}')" || echo "Could not get book count"

echo "Populating the database..."
# Always run database population to catch any previously skipped books
python manage.py populate_database || handle_error "Database population failed"
echo "Database population completed"

echo "Checking final book count..."
python -c "from core.models import Book; print(f'Final book count: {Book.objects.count()}')" || echo "Could not get book count"

echo "Collecting static files..."
python manage.py collectstatic --noinput || handle_error "Static files collection failed"
echo "Static files collected successfully"

echo "========== Starting server =========="
exec gunicorn app.wsgi:application --bind 0.0.0.0:8000