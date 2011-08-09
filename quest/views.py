from django.conf import settings
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
from utils.decorators import is_post
from utils.emailer import new_anwer_emailer
from quest.messages import QUESTION_POSTING_SUCCESSFUL

def view_all_questions(request, all_questions_template):
    questions = Question.objects.all().order_by('-modified_on')
    #FIXME/TODO:This has to be cached at all costs
    all_tags = TaggedItem.tags_for(Question)
    return response(request, all_questions_template, {'questions':questions, 'all_tags':all_tags})

def view_question(request, question_id, question_slug, question_template):
    question = get_object_or_404(Question, id=int(question_id))#question_slug is for SEO
    if question.is_accepting_answers():
        give_answer_form = GiveAnswerForm()
    else:
        give_answer_form = None
    return response(request, question_template, {'question':question, 'give_answer_form':give_answer_form})

@login_required
@is_post
def view_close_answering(request, question_template, close_answer_template):#This would be an ajax post call
    question_id = post_data(request).get('question_id')
    question = get_object_or_404(Question, id=int(question_id))
    userprofile = loggedin_userprofile(request)
    if userprofile.id == question.owner.id:
        question.close_answering()
        return response(request, close_answer_template, {'give_answer_form':None})
    raise Http404

@login_required
@is_post
def view_accept_answer(request, question_id, answers_template):
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
    userprofile = loggedin_userprofile(request)
    asked_questions = userprofile.asked_questions
    if request.method == 'GET':
        form = AskQuestionForm()
        return response(request, ask_question_template, {'form':form,
                                                         'asked_questions':asked_questions})
    form = AskQuestionForm(post_data(request))
    if form.is_valid():
        question = Question.objects.create_question(title=form.cleaned_data.get('title'),
                                                    description=form.cleaned_data.get('description'),
                                                    userprofile=userprofile,
                                                    tags=form.cleaned_data.get('tags'))
        messages.success(request, QUESTION_POSTING_SUCCESSFUL)
        return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_question', args=(question.id, question.slug)))
    return response(request, ask_question_template, {'form':form,
                                                     'asked_questions':asked_questions})

@login_required
def view_edit_question(request, question_id, question_slug, edit_question_template):
    userprofile = loggedin_userprofile(request)
    question = get_object_or_404(Question, id=int(question_id))
    if userprofile.is_my_question(question):
        asked_questions = list(userprofile.asked_questions)
        for question_info in asked_questions:
            if question_info['id'] == int(question_id):
                asked_questions.remove({'title':question.title,
                                        'id':int(question_id),
                                        'slug':question_slug})
        
        if request.method == 'GET':
            question_data = {'title':question.title,
                             'description':question.description,
                             'tags':",".join([tag['name'] for tag in question.tags.values('name')])}
            form = AskQuestionForm(question_data)
            return response(request, edit_question_template, {'form':form,
                                                              'question':question,
                                                              'previous_questions':asked_questions})
        form = AskQuestionForm(post_data(request))
        if form.is_valid():
            Question.objects.update_question(question,
                                             title=form.cleaned_data.get('title'),
                                             description=form.cleaned_data.get('description'),
                                             tags=form.cleaned_data.get('tags'))
            from quest.messages import QUESTION_UPDATED_SUCCESSFULLY
            messages.success(request, QUESTION_UPDATED_SUCCESSFULLY)
            return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_question', args=(question.id, question.slug)))
        return response(request, edit_question_template, {'form':form,
                                                          'question':question,
                                                          'previous_questions':asked_questions})
    raise Http404

@login_required
def view_give_answer(request, question_id, give_answer_template, question_template):
    question = get_object_or_404(Question, id=int(question_id))
    if request.method == 'POST':
        form = GiveAnswerForm(post_data(request))
        if form.is_valid():
            userprofile = loggedin_userprofile(request)
            new_answer = Answer.objects.create_answer(question=question,
                                                      description=form.cleaned_data.get('description'),
                                                      userprofile=userprofile)
            new_anwer_emailer(question, new_answer)
            from quest.messages import ANSWER_POSTING_SUCCESSFUL
            messages.success(request, ANSWER_POSTING_SUCCESSFUL)
            give_answer_form = GiveAnswerForm()
            return response(request, question_template, {'question':question, 'give_answer_form':give_answer_form})
        return response(request, question_template, {'question':question, 'give_answer_form':form})
    return HttpResponseRedirect(redirect_to=url_reverse('quest.views.view_question', args=(question.id, question.slug)))

def view_tagged_questions(request, tag_name, tagged_questions_template):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.filter(tags__name__in=[tag_name]).values('id', 'slug', 'title')
    paginator = Paginator(questions, settings.DEFAULT_PAGINATION_COUNT)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        questions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)
    #FIXME/TODO:This has to be cached at all costs
    all_tags = TaggedItem.tags_for(Question)
    return response(request, tagged_questions_template, {'questions': questions.object_list,
                                                        'tag': tag,
                                                        'all_tags':all_tags})
