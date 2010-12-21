from django.conf import settings
from django.core.urlresolvers import reverse as url_reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.test import TestCase
from django.template.defaultfilters import slugify
import shutil
import os
from users.models import User, UserProfile

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
    settings.DOCSTORE_CONFIG['files_storage_path'] = "/".join([os.path.dirname(settings.ROOT_PATH), 'test_stud2dotoh_uploaded_files'])
    def tearDown(self):
        del self.client
        
    def login_as(self, email, password):
        return self.client.post(path=url_reverse('users.views.view_login'),
                                data={'email':email, 'password':password})
        
    def logout(self):
        return self.client.post(path=url_reverse('users.views.view_logout'))
    
    def setUp(self):
        try:
            shutil.rmtree(settings.DOCSTORE_CONFIG['files_storage_path'])
        except OSError:
            pass
        os.mkdir(settings.DOCSTORE_CONFIG['files_storage_path'])
    
def loggedin_userprofile(request):
    return request.user.get_profile()

def get_user_directory_path(userprofile):
    #TODO:Raise a deprecation warning about the usage of this method. Use userprofile.user_directory_path
    return "/".join([settings.DOCSTORE_CONFIG['files_storage_path'], str(userprofile.id)])

def set_userprofile_in_context(request):
    return {'userprofile':request.user.get_profile()}