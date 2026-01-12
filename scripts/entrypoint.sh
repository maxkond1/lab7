#!/bin/sh
# entrypoint.sh — wait for DB then run migrations and gunicorn
set -e

# Ensure defaults (can be overridden via .env / environment)
: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"

# Wait for Postgres and then run Django commands
./scripts/wait_for_db.sh "${DB_HOST}:${DB_PORT}" python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn polls_proj.wsgi:application --bind 0.0.0.0:8000
