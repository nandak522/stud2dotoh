from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect, Http404
from utils import response, post_data, loggedin_userprofile
from django.shortcuts import get_object_or_404
from django.contrib import messages
from quest.models import Question, Answer
from quest.forms import AskQuestionForm, GiveAnswerForm
from taggit.models import Tag, TaggedItem
from django.core.paginator import Paginator

def view_all_questions(request, all_questions_template):
    questions = Question.objects.all().order_by('-modified_on')
    return response(request, all_questions_template, {'questions':questions})

def view_question(request, question_id, question_slug, question_template):
    question = get_object_or_404(Question, id=int(question_id))#question_slug is for SEO
    if question.is_accepting_answers():
        give_answer_form = GiveAnswerForm()
    else:
        give_answer_form = None
    return response(request, question_template, {'question':question, 'give_answer_form':give_answer_form})

@login_required
def view_close_answering(request, question_template, close_answer_template):#This would be an ajax post call
    if request.method == 'POST':
        question_id = post_data(request).get('question_id')
        question = get_object_or_404(Question, id=int(question_id))
        userprofile = loggedin_userprofile(request)
        if userprofile.id == question.owner.id:
            question.close_answering()
            return response(request, close_answer_template, {'give_answer_form':None})
    raise Http404

@login_required
def view_accept_answer(request, question_id, answers_template):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=int(question_id))
        userprofile = loggedin_userprofile(request)
        if userprofile.id == question.owner.id:
            answer_id = post_data(request).get('answer_id')
            answer = get_object_or_404(Answer, id=int(answer_id))
            answer.accept(userprofile)
            return response(request, answers_template, {'question':question, 'all_answers':question.answers})
    raise Http404

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
                                                    userprofile=userprofile,
                                                    tags=form.cleaned_data.get('tags'))
        from quest.messages import QUESTION_POSTING_SUCCESSFUL
        messages.success(request, QUESTION_POSTING_SUCCESSFUL)
        return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_question', args=(question.id, question.slug)))
    return response(request, ask_question_template, {'form':form})

def view_email_question(request, question_id, question_slug, email_question_template):
    raise NotImplementedError

@login_required
def view_edit_question(request, question_id, question_slug, edit_question_template):
    question = get_object_or_404(Question, id=int(question_id))
    if question.owner.id != loggedin_userprofile(request).id:
        from quest.messages import QUESTION_UPDATION_DISALLOWED
        messages.success(request, QUESTION_UPDATION_DISALLOWED)
        return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_question', args=(question.id, question.slug)))
    if request.method == 'GET':
        question_data = {'title':question.title,
                         'description':question.description,
                         'tags':",".join([tag['name'] for tag in question.tags.values('name')])}
        form = AskQuestionForm(question_data)
        return response(request, edit_question_template, {'form':form, 'question':question})
    form = AskQuestionForm(post_data(request))
    if form.is_valid():
        Question.objects.update_question(question,
                                         title=form.cleaned_data.get('title'),
                                         description=form.cleaned_data.get('description'),
                                         tags=form.cleaned_data.get('tags'))
        from quest.messages import QUESTION_UPDATED_SUCCESSFULLY
        messages.success(request, QUESTION_UPDATED_SUCCESSFULLY)
        return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_question', args=(question.id, question.slug)))
    return response(request, edit_question_template, {'form':form, 'question':question})

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

def view_tagged_questions(request, tag_name, tagged_questions_template):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.filter(tags__name__in=[tag_name])
    paginator = Paginator(questions, 1)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        questions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)
    return response(request, tagged_questions_template, {'questions': questions.object_list,
                                                        'tag': tag})