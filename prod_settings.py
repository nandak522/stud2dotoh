rom settings import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'madhavbnk_stud2dotoh',                      # Or path to database file if using sqlite3.
        'USER': 'madhavbnk_stud2dotoh',                      # Not used with sqlite3.
        'PASSWORD': '1c7bac12',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'utils.middlewares.StatsMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'users',
    'quest',
    'taggit'
)

EMAIL_SUBJECT_PREFIX = '[Stud2.0]'

AUTH_PROFILE_MODULE = 'users.UserProfile'

MEDIA_ROOT = '/home/madhavbnk/webapps/stud2dotoh/stud2dotoh/site_media/'

