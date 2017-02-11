# Configures settings for testing Django with Pytest
# http://www.johnmcostaiii.net/2013/django-projects-to-django-apps-converting-the-unit-tests/
from wsdproject.settings.base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        }
}
