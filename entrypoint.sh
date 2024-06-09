#!/bin/sh

wait_for_db() {
    echo "Waiting for $1..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "$1 started"
}

if [ "$DB_NAME" = "postgres" ]; then
    wait_for_db "postgres"
fi

python manage.py migrate

exec "$@"