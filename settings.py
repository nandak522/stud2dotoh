import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('NandaKishore', 'madhav.bnk@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'stud2dotoh',                      # Or path to database file if using sqlite3.
        'USER': 'stud2dotoh',                      # Not used with sqlite3.
        'PASSWORD': 'stud2dotoh',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'sqlite3' 
    DATABASES['default']['NAME'] = 'stud2dotoh.db'

TIME_ZONE = 'Asia/Calcutta'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

USE_L10N = True

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
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

ROOT_URLCONF = '%s.urls' % PROJECT_FOLDER_NAME

TEMPLATE_DIRS = (
                 '%s/templates' % PROJECT_FOLDER_NAME,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'debug_toolbar',
    'users'
)

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

EMAIL_SUBJECT_PREFIX = '[Stud2.0] '