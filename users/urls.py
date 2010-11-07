from django.conf.urls.defaults import *

urlpatterns = patterns('users.views',
    (r'^$', 'view_all_users', {'all_users_template':'all_users.html'}, 'all_users'),
    (r'^(?P<user_id>\d+)/(?P<user_slug_name>[\w\s-]+)/$', 'view_userprofile', {'userprofile_template':'user_profile.html'}, 'user_profile'),
    (r'^(?P<filename>[\w\s-]+)/$', 'view_file_content_view', {}, 'file_content_view_link'),
    (r'^questions/ask/$', 'view_ask_question', {'question_template':''}, 'ask_question'),
    (r'^questions/$', 'view_questions', {'questions_template':''}, 'questions'),
)