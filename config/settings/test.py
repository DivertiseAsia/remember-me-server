from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TEST_DJANGO_SECRET_KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'circle_test',
        'USER': 'ubuntu',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
