from utils.decorators import is_ajax
from taggit.models import Tag
from django.utils import simplejson
from django.http import HttpResponse
from users.models import College, Company
from quest.models import Question
from django.core.urlresolvers import reverse

@is_ajax
def view_ajax_objects_list(request, query_context):
    term = request.GET.get('term')
    if query_context == 'college':
        objects = College.objects.filter(name__istartswith=term).values('id', 'name')
        items = [{'id':object_info['id'], 'value':object_info['name']} for object_info in objects]
    elif query_context == 'company':
        objects = Company.objects.filter(name__istartswith=term).values('id', 'name')
        items = [{'id':object_info['id'], 'value':object_info['name']} for object_info in objects]
    elif query_context == 'tag':
        objects = Tag.objects.filter(name__istartswith=term).values('id', 'name')
        items = [{'id':object_info['id'], 'value':object_info['name']} for object_info in objects]
    elif query_context == 'question':
        objects = Question.objects.filter(title__icontains=term).values('id', 'title', 'slug')
        items = [{'id':object_info['id'], 'label':object_info['title'], 'value':reverse('quest.views.view_question', args=(object_info['id'], object_info['slug']))} for object_info in objects]
    return HttpResponse(simplejson.dumps(items), mimetype='application/json')
