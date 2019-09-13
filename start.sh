#!/usr/bin/env bash

echo "RememberME start!"
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py init_super_user
gunicorn --bind :8001 server.wsgi:application --daemon --workers 3 --timeout 3600
nginx -g "daemon off;"