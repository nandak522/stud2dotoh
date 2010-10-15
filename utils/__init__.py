from django.core.urlresolvers import reverse as url_reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.test import TestCase

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
        
    def login_as(self, email, password):
        response = self.client.post(path=url_reverse('users.views.view_login'),
                                    data={'email':email, 'password':password})
        return response