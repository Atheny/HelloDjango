#!/bin/sh
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn HelloDjango.wsgi:application -w 4 -k gthread -b 127.0.0.1:8000 --chdir=/app