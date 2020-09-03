import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '^(80*3o029djtpnslc^b9dyy^yaxlcs%2xbmw5^_owpte4vvk1'

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "18.222.148.211"]



postgresql = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbms_db',
        'USER': 'dbms',
        'PASSWORD': 'some_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

sqlite = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = postgresql

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
