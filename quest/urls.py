from django.conf.urls.defaults import *

urlpatterns = patterns('quest.views',
    (r'^$', 'view_questions', {'questions_template':''}, 'questions'),
    (r'^ask/$', 'view_ask_question', {'question_template':''}, 'ask_question'),
)