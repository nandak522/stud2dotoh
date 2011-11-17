from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'stud2dotoh',                      # Or path to database file if using sqlite3.
        'USER': 'stud2dotoh',                      # Not used with sqlite3.
        'PASSWORD': 'stud2dotoh',                  # Not used with sqlite3.
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
#    'utils.middlewares.StatsMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'extensions',
#    'debug_toolbar',
    'users',
    'quest',
    'taggit',#Ideally this should be a submodule
)


EMAIL_SUBJECT_PREFIX = '[Stud2.0] '

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'donot-reply@stud2dotoh.com'
EMAIL_HOST_PASSWORD = '1c7bac12'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AUTH_PROFILE_MODULE = 'users.UserProfile'

MEDIA_ROOT = '/home/madhavbnk/webapps/stud2dotoh/stud2dotoh/site_media/'

SEND_BROKEN_LINK_EMAILS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ROOT_URLCONF = 'urls'

USE_I18N = False

USE_L10N = False

TEMPLATE_DIRS = (
                 '/home/madhavbnk/webapps/stud2dotoh/stud2dotoh/templates',
)

NOTE_POINTS = 3

QUESTION_POINTS = 3

ANSWER_POINTS = 5

