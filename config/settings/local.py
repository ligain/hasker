import datetime

from .base import *

DEBUG = True

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
    }
}

SECRET_KEY = get_env_variable('SECRET_KEY')

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=5),
}

REST_FRAMEWORK['PAGE_SIZE'] = 2
