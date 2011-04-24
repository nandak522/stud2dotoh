from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'madhavbnk_labs_stud2dotoh', # Or path to database file if using sqlite3.
        'USER': 'madhavbnk_labs_stud2dotoh', # Not used with sqlite3.
        'PASSWORD': '5ef7b9a7', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
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
    'debug_toolbar.middleware.DebugToolbarMiddleware'
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
    'taggit',
    'debug_toolbar'
)

EMAIL_SUBJECT_PREFIX = '[Stud2.0 Labs]'

AUTH_PROFILE_MODULE = 'users.UserProfile'

MEDIA_ROOT = '/home/madhavbnk/webapps/labs_stud2dotoh/labs/site_media/'

ROOT_URLCONF = 'urls'

USE_I18N = False

USE_L10N = False

TEMPLATE_DIRS = (
                 '/home/madhavbnk/webapps/labs_stud2dotoh/labs/templates',
                 )