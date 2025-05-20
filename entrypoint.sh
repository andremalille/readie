#!/bin/sh
set -e

echo "Waiting for database..."
python manage.py wait_for_db

echo "Creating a superuser..."
python manage.py ensure_superuser

echo "Applying database migrations..."
python manage.py migrate

echo "Populating the database..."
python manage.py populate_database

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec gunicorn app.wsgi:application --bind 0.0.0.0:8000
