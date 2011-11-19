SITE_DIR = '/home/ubuntu/webapps/stud2dotoh/'
import site
site.addsitedir(SITE_DIR) 

import os
import sys
sys.path.append(SITE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'prod_settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
