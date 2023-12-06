#!/usr/bin/env bash

echo "RememberME start!"
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py init_super_user
python manage.py runserver 0.0.0.0:8000
