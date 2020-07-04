import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Изменить ручками что то в нем
SECRET_KEY = '^(80*3o029zmqkwlxa^b9dyy^yaxlcs%2xbmw5^_owpte4vvk1'

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project360',
        'USER': 'userdb',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
