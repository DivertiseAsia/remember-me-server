import os
import psycopg2
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ORIGIN_PROTOCOL = 'https'
ORIGIN_URL = 'rememberme-server.herokuapp.com'

ALLOWED_HOSTS = [ORIGIN_URL]
CORS_ORIGIN_WHITELIST = ['https://rememberme-38415.web.app']

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

SUPER_PASSWORD = os.environ.get('SUPER_PASSWORD', 'RememberME1234')

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', 'SG.PLEASE_ADD_SENDGRID_API_KEY')
DEV_EMAIL = os.environ.get('DEV_EMAIL', 'dev@divertise.asia')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'hunter@divertise.asia')

import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
