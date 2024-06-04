#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py test
python manage.py crontab add
exec gunicorn libary.wsgi:application --bind 0.0.0.0:8000
