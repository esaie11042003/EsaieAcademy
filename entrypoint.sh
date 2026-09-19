#!/bin/bash
set -e

echo "Applying migrations..."
python manage.py migrate --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Ensuring superuser exists..."
    python manage.py createsuperuser --noinput || true
fi

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
