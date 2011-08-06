from django.conf.urls.defaults import *

urlpatterns = patterns('utils.views',
    (r'^colleges_ajax/$', 'view_ajax_objects_list', {'query_context':'college'}, 'ajax_colleges_list'), 
    (r'^companies_ajax/$', 'view_ajax_objects_list', {'query_context':'company'}, 'ajax_companies_list'), 
    (r'^tags_ajax/$', 'view_ajax_objects_list', {'query_context':'tag'}, 'ajax_tags_list'),
    (r'^questions_ajax/$', 'view_ajax_objects_list', {'query_context':'question'}, 'ajax_questions_list'),
)
