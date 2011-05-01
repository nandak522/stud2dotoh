from settings import *

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': ':memory:'}
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.transaction.TransactionMiddleware',
    'utils.middlewares.StatsMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'extensions',
    'users',
    'quest',
    'taggit'#Ideally this should be a submodule
)