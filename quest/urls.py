from django.conf.urls.defaults import *

urlpatterns = patterns('quest.views',
    (r'^$', 'view_all_questions', {'all_questions_template':'all_questions.html'}, 'all_questions'),
    (r'^(?P<question_id>\d+)/giveanswer/$', 'view_give_answer', {'give_answer_template':'give_answer.html', 'question_template':'question.html'}, 'give_answer'),
    (r'^(?P<question_id>\d+)/acceptanswer/$', 'view_accept_answer', {'answers_template':'answers.html'}, 'accept_answer'),
    (r'^closeanswering/$', 'view_close_answering', {'question_template':'question.html', 'close_answer_template':'give_answer.html'}, 'close_answering'),
    (r'^(?P<question_id>\d+)/(?P<question_slug>[\w\s-]+)/$', 'view_question', {'question_template':'question.html'}, 'question'),
    (r'^(?P<question_id>\d+)/(?P<question_slug>[\w\s-]+)/edit/$', 'view_edit_question', {'edit_question_template':'ask_or_edit_question.html'}, 'edit_question'),
    (r'^ask/$', 'view_ask_question', {'ask_question_template':'ask_or_edit_question.html'}, 'ask_question'),
    (r'^(?P<tag_name>[\w-]+)/$', 'view_tagged_questions', {'tagged_questions_template':'all_questions.html'}, 'tagged_questions'),
)