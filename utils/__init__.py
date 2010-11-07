from django.conf import settings
from django.core.urlresolvers import reverse as url_reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.test import TestCase
from django.template.defaultfilters import slugify

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
    def tearDown(self):
        del self.client
        
    def login_as(self, username, password):
        return self.client.post(path=url_reverse('users.views.view_login'),
                                data={'username':username, 'password':password})
    
def loggedin_userprofile(request):
    return request.user.get_profile()

def get_user_directory_path(userprofile):
    return "/".join([settings.DOCSTORE_CONFIG['files_storage_path'], str(userprofile.id)])