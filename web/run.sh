#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput -c
exec gunicorn blog.wsgi:application --bind 0.0.0.0:8008 "$@"
