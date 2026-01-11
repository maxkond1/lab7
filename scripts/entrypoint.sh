#!/bin/sh
# entrypoint.sh — wait for DB then run migrations and gunicorn
set -e

./scripts/wait_for_db.sh "$DB_HOST" python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn polls_proj.wsgi:application --bind 0.0.0.0:8000
