from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from users.models import UserProfile
from utils import response, post_data, loggedin_userprofile, slugify
from users.decorators import anonymoususer
from django.shortcuts import get_object_or_404
from django.contrib import messages
from quest.models import Question, Answer
from quest.forms import AskQuestionForm, GiveAnswerForm

def view_all_questions(request, all_questions_template):
    questions = Question.objects.all()
    return response(request, all_questions_template, {'questions':questions})

def view_question(request, question_id, question_slug, question_template):
    question = get_object_or_404(Question, id=int(question_id), slug=question_slug)
    give_answer_form = GiveAnswerForm()
    return response(request, question_template, {'question':question, 'give_answer_form':give_answer_form})

@login_required
def view_ask_question(request, ask_question_template):
    if request.method == 'GET':
        form = AskQuestionForm()
        return response(request, ask_question_template, {'form':form})
    form = AskQuestionForm(post_data(request))
    if form.is_valid():
        userprofile = loggedin_userprofile(request)
        question = Question.objects.create_question(title=form.cleaned_data.get('title'),
                                                    description=form.cleaned_data.get('description'),
                                                    userprofile=userprofile)
        from quest.messages import QUESTION_POSTING_SUCCESSFUL
        messages.success(request, QUESTION_POSTING_SUCCESSFUL)
        return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_question', args=(question.id, question.slug)))
    return response(request, ask_question_template, {'form':form})

@login_required
def view_give_answer(request, question_id, give_answer_template, question_template):
    question = get_object_or_404(Question, id=int(question_id))
    if request.method == 'POST':
        form = GiveAnswerForm(post_data(request))
        if form.is_valid():
            userprofile = loggedin_userprofile(request)
            Answer.objects.create_answer(question=question,
                                         description=form.cleaned_data.get('description'),
                                         userprofile=userprofile)
            from quest.messages import ANSWER_POSTING_SUCCESSFUL
            messages.success(request, ANSWER_POSTING_SUCCESSFUL)
            give_answer_form = GiveAnswerForm()
            return response(request, question_template, {'question':question, 'give_answer_form':give_answer_form})
        return response(request, question_template, {'question':question, 'give_answer_form':form})
    return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_question', args=(question.id, question.slug)))