from django.conf import settings
from django.contrib.sites.models import Site 
from django.core.urlresolvers import reverse as url_reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.test import TestCase
import os
import shutil

def response(request, template, context):
    return render_to_response(template, context, context_instance=RequestContext(request))

def print_json(queryset):
    from django.core.serializers import serialize
    print serialize("json", queryset, indent=4)

def post_data(request):
    return request.POST.copy()

def get_data(request):
    return request.GET.copy()

class TestCase(TestCase):
    def setUp(self):
        settings.DEBUG = True
    
    def tearDown(self):
        del self.client
        
    def login_as(self, email, password):
        return self.client.post(path=url_reverse('users.views.view_login'),
                                data={'email':email, 'password':password})
        
    def logout(self):
        return self.client.post(path=url_reverse('users.views.view_logout'))
    
def loggedin_userprofile(request):
    return request.user.get_profile()

def useful_params_in_context(request):
    params = {}
    params['site'] = Site.objects.get(id=settings.SITE_ID)
    if request.user.is_authenticated():
        params['userprofile'] = request.user.get_profile()
        params['userprofilegroup'] = request.user.get_profile().group_name
    #TODO:the entire params dict needs to be cached
    return params

def get_stats():
    #TODO:This import is not moved to the global level, as there is a
    #circular import problem. But for every page this import will be happening :'(
    from users.models import College, Group, Company
    stats = {'colleges_count':College.objects.count(),
             'students_count':Group.objects.get(name='Student').user_set.count(),
             'companies_count':Company.objects.count(),
             'employees_count':Group.objects.get(name='Employee').user_set.count()}
    return stats