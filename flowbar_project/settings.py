"""
Django settings for flowbar_project project.
Generado con Django 4.2.26
"""

from pathlib import Path
from decouple import config
import dj_database_url
import os
import pymysql

# Necesario para usar MySQL en Django
pymysql.install_as_MySQLdb()

# ---------------------------------
# BASE DIR
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------
# SECURITY
# ---------------------------------
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

# Railway requiere permitir wildcard
ALLOWED_HOSTS = ['*']


# ---------------------------------
# APPS
# ---------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps del proyecto
    'users',
    'menu',
    'orders',

    # Terceros
    'widget_tweaks',
]


# ---------------------------------
# MIDDLEWARE
# ---------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # (coma agregada)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ---------------------------------
# ROOT + WSGI
# ---------------------------------
ROOT_URLCONF = 'flowbar_project.urls'
WSGI_APPLICATION = 'flowbar_project.wsgi.application'


# ---------------------------------
# TEMPLATES
# ---------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ---------------------------------
# DATABASE (Railway MySQL)
# ---------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=config(
            'DATABASE_URL',
            default='mysql://root:password@localhost/proyecto'
        ),
        conn_max_age=600,
        ssl_require=False
    )
}


# ---------------------------------
# AUTH USER MODEL
# ---------------------------------
AUTH_USER_MODEL = 'users.User'


# ---------------------------------
# PASSWORD VALIDATION
# ---------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------
# LOCALIZATION
# ---------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---------------------------------
# STATIC (Whitenoise)
# ---------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ---------------------------------
# LOGIN / LOGOUT
# ---------------------------------
LOGIN_REDIRECT_URL = 'login_success'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'


# ---------------------------------
# CSRF – necesario para Railway
# ---------------------------------
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]


# ---------------------------------
# DEFAULT PRIMARY KEY
# ---------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

