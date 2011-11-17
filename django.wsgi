import os,sys

project = os.path.dirname(os.path.dirname(__file__))
workspace = os.path.dirname(project)
sys.path.append(workspace)

os.environ['DJANGO_SETTINGS_MODULE'] = 'prod_settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
