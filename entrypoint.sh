#!/bin/sh
set -e

echo "Waiting for PostgreSQL at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."

until python - <<'PY'
import os, sys
import psycopg2
try:
    psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "ughe_db"),
        user=os.getenv("POSTGRES_USER", "ughe_user"),
        password=os.getenv("POSTGRES_PASSWORD", "ughe_secure_password"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
except Exception as exc:
    print(exc)
    sys.exit(1)
sys.exit(0)
PY
do
  echo "PostgreSQL is unavailable — sleeping"
  sleep 2
done

echo "PostgreSQL is ready."

python manage.py makemigrations content --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_data

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
