import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Изменить ручками что то в нем
SECRET_KEY = '^(80*3o029zmqkwlxa^b9dyy^uifbnuis^ldl*((bmw5^_owpte4vvk1'

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'admin',
        'USER': 'userdb',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#STATIC_DIR = os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
