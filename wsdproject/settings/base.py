"""
Django settings for wsdproject project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import logging.config
import os

import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(__file__)
for _ in range(3):
    BASE_DIR = os.path.dirname(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*5wm+_=gsjd@l@cbvx)bv!^78f*v)cvm=5hgju_p7u%%v2#c90'

# SECURITY WARNING: don't run with debug turned on in production!
# Configured in dev.py and prod.py
# DEBUG = True

ALLOWED_HOSTS = []


# Application definition

PROJECT_APPS = [
    'bootstrap3',
    'gamestore',
    'django_extensions',
    'haystack',
]

PREREQ_APPS = [
    'django.contrib.admin',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Project apps should be loaded before prereq apps!
INSTALLED_APPS = PROJECT_APPS + PREREQ_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wsdproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'wsdproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# TODO: PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


# Media (user uploads) files
# https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-MEDIA_ROOT
MEDIA_DIR = 'media'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_DIR)


# Registration
# https://django-registration-redux.readthedocs.io/en/latest/quickstart.html
ACCOUNT_ACTIVATION_DAYS = 3
REGISTRATION_AUTO_LOGIN = True


# Setup logging config from `logging.yaml` file.
LOGGING_CONFIG = None
LOGGING_FILE = os.path.join(BASE_DIR, 'logging.yaml')  # logging config file
LOG_DIR = os.path.join(BASE_DIR, '.logs')  # Directory to save log files

with open(LOGGING_FILE, 'rt') as file:
    LOGGING_DICT = yaml.safe_load(file.read())

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

for name in LOGGING_DICT['handlers']:
    handler = LOGGING_DICT['handlers'][name]
    if 'filename' in handler:
        handler['filename'] = os.path.join(LOG_DIR, handler['filename'])

logging.config.dictConfig(LOGGING_DICT)


# Search Engine
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
