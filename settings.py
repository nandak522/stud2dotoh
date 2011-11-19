import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admins', 'coreteam@stud2dotoh.com'),
)

MANAGERS = ADMINS

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'stud2dotoh.db',
        }
    }
else:
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

TIME_ZONE = 'Asia/Calcutta'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

USE_L10N = False

ROOT_PATH = os.getcwd()

PROJECT_FOLDER_NAME = ROOT_PATH.split('/')[-1]

MEDIA_ROOT = '%s/site_media/' % ROOT_PATH

ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-89vmzalke_spvjj44w4x9&*34bpf)0s^t3w&jr^7das#*jz)f'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

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

ROOT_URLCONF = '%s.urls' % PROJECT_FOLDER_NAME

TEMPLATE_DIRS = (
                 '%s/templates' % ROOT_PATH,
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

#DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

EMAIL_SUBJECT_PREFIX = '[Stud2.0] '

AUTH_PROFILE_MODULE = 'users.UserProfile'

INTERNAL_IPS = ('127.0.0.1', )

FILTER_HTML_TAGS = "script button input marquee style"

AUTHENTICATION_BACKENDS = ('utils.backends.EmailAuthBackend',
                           'django.contrib.auth.backends.ModelBackend')

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.contrib.messages.context_processors.messages",
                               "utils.useful_params_in_context")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_PAGINATION_COUNT = 25

NOTE_POINTS = 3

QUESTION_POINTS = 3

ANSWER_POINTS = 5
