#!/bin/sh

set -e

echo "Waiting for database..."
python manage.py wait_for_db

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn app.wsgi:application --bind 0.0.0.0:8000
