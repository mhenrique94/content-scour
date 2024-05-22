#!/bin/bash

if [ "$DB_NAME" = "djangoec2" ]
then
    echo "Aguardando RDS postgreSQL..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "RDS PostgreSQL iniciado!"
fi

exec gunicorn contentscour.wsgi:application --bind 0.0.0.0:8000