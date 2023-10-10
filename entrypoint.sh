#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

exec "$@"

exec chmod +x /app/webapp/run_tests.sh

# Inicia el servidor de Django
exec hupper -m django runserver 0.0.0.0:8000
