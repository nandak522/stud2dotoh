from utils import TestCase
from django.core.urlresolvers import reverse as url_reverse
from users.models import UserProfile
from quest.models import Question, Answer
from django.conf import settings

class AllQuestionsPageTests(TestCase):
    fixtures = ['users.json', 'questions.json', 'answers.json']

    def test_all_questions_page_anonymous_access(self):
        response = self.client.get(url_reverse('quest.views.view_all_questions'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_questions.html')
        context = response.context[0]
        self.assertTrue(context.has_key('questions'))
        self.assertTrue(context.get('questions'))

    def test_all_questions_page_authenticated_access(self):
        self.login_as(username='madhavbnk', password='nopassword')
        response = self.client.get(url_reverse('quest.views.view_all_questions'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_questions.html')
        context = response.context[0]
        self.assertTrue(context.has_key('questions'))
        self.assertTrue(context.get('questions'))

class QuestionPageTests(TestCase):
    fixtures = ['users.json', 'questions.json', 'answers.json']

    def test_each_question_page_fresh_access(self):
        question = Question.objects.latest()
        response = self.client.get(url_reverse('quest.views.view_question', args=(question.id, question.slug)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'question.html')
        context = response.context[0]
        self.assertTrue(context.has_key('question'))
        self.assertTrue(context.get('question'))
        question = context.get('question')
        self.assertTrue(question.answers)

    def test_invalid_url_to_question_page(self):
        question = Question.objects.latest()
        response = self.client.get(url_reverse('quest.views.view_question', args=(0, question.slug)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 404)

    def test_close_answering_a_question_by_non_owner(self):
        question = Question.objects.latest()
        self.login_as(username='somerandomuser', password='nopassword')
        response = self.client.post(url_reverse('quest.views.view_close_answering'), {'question_id':question.id})
        self.assertTrue(response)
        self.assertEquals(response.status_code, 404)

    def test_close_answering_a_question_by_owner(self):
        question = Question.objects.latest()
        self.login_as(username='madhavbnk', password='nopassword')
        response = self.client.post(url_reverse('quest.views.view_close_answering'), {'question_id':question.id})
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'give_answer.html')
        self.assertFalse(Question.objects.get(id=question.id).is_accepting_answers())
        context = response.context
        give_answer_form = context.get('give_answer_form')
        self.assertFalse(give_answer_form)

    def test_accept_an_answer_for_a_question_by_non_owner(self):
        question = Question.objects.latest()
        answer = question.answers[0]
        self.login_as(username='somerandomuser', password='nopassword')
        response = self.client.post(url_reverse('quest.views.view_accept_answer', args=(question.id,)), data={'question_id':question.id, 'answer_id':answer.id})
        self.assertTrue(response)
        self.assertEquals(response.status_code, 404)
        self.assertFalse(Answer.objects.get(id=answer.id).accepted)

    def test_accept_an_answer_for_a_question_by_owner(self):
        question = Question.objects.latest()
        answer = question.answers[0]
        self.login_as(username='madhavbnk', password='nopassword')
        response = self.client.post(url_reverse('quest.views.view_accept_answer', args=(question.id,)), data={'question_id':question.id, 'answer_id':answer.id})
        self.assertTrue(response)
        self.assertTrue(Answer.objects.get(id=answer.id).accepted)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'answers.html')

    def test_unaccepting_an_answer_of_a_question(self):
        question = Question.objects.latest()
        answer = question.answers[0]
        self.login_as(username='madhavbnk', password='nopassword')
        response = self.client.post(url_reverse('quest.views.view_accept_answer', args=(question.id,)), data={'question_id':question.id, 'answer_id':answer.id})
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'answers.html')
        self.assertTrue(Answer.objects.get(id=answer.id).accepted)
        answer = question.answers[1]
        response = self.client.post(url_reverse('quest.views.view_accept_answer', args=(question.id,)), data={'question_id':question.id, 'answer_id':answer.id})
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'answers.html')
        self.assertTrue(Answer.objects.get(id=answer.id).accepted)

class AskQuestionTests(TestCase):
    fixtures = ['users.json']

    def test_ask_question_page_anonymous_access(self):
        response = self.client.get(url_reverse('quest.views.view_ask_question'))
        self.assertTrue(response)
        self.assertRedirects(response,
                             expected_url='/accounts/login/?next=/questions/ask/',
                             status_code=302,
                             target_status_code=200)

    def test_ask_question_page_authenticated_access(self):
        self.login_as(username='madhavbnk', password='nopassword')
        response = self.client.get(url_reverse('quest.views.view_ask_question'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ask_question.html')
        context = response.context[0]
        self.assertTrue(context.has_key('form'))
        ask_question_form = context.get('form')
        self.assertFalse(ask_question_form.errors)

    def test_asking_a_question(self):
        self.login_as(username='madhavbnk', password='nopassword')
        question_data = {'title':'How is Stud2dotoh Hiring ?',
                         'description':'Just interested in the process of hiring for Stud2dotoh'}
        old_questions_count = Question.objects.count()
        response = self.client.post(url_reverse('quest.views.view_ask_question'), question_data)
        new_questions_count = Question.objects.count()
        self.assertEquals(new_questions_count, old_questions_count + 1)
        question = Question.objects.latest()
        self.assertTrue(question)
        self.assertEquals(question.title, question_data['title'])
        self.assertEquals(question.description, question_data['description'])
        self.assertEquals(UserProfile.objects.get(user__username='madhavbnk').id, question.raised_by.id)
        self.assertRedirects(response,
                             expected_url=url_reverse('quest.views.view_question', args=(question.id, question.slug)),
                             status_code=302,
                             target_status_code=200)

    def test_asking_a_question_with_xss(self):
        self.login_as(username='madhavbnk', password='nopassword')
        question_data = {'title':'How is Stud2dotoh Hiring ?',
                         'description':'Stud2dotoh! <script>alert("I will shoot you in the head")</script>'}
        response = self.client.post(url_reverse('quest.views.view_ask_question'), question_data)
        question = Question.objects.latest()
        self.assertRedirects(response,
                             expected_url=url_reverse('quest.views.view_question', args=(question.id, question.slug)),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(url_reverse('quest.views.view_question', args=(question.id, question.slug)))
        self.assertTrue(response)
        context = response.context[0]
        question = context.get('question')
        question_description = question.description
        self.assertTrue(question_description)
        self.assertFalse(question_data['description'] in question_description)
        self.assertFalse('<script>' in question_description)

    def test_asking_a_question_with_blocked_tags(self):
        self.login_as(username='madhavbnk', password='nopassword')
        question_data = {'title':'How is Stud2dotoh Hiring ?',
                         'description':'Stud2dotoh! <script>alert("I will shoot you in the head")</script><input type=\'text\' name=\'head_name\' value=\'Your Name\'/><marquee>I am big distracting rolling banner</marquee>'}
        response = self.client.post(url_reverse('quest.views.view_ask_question'), question_data)
        question = Question.objects.latest()
        response = self.client.get(url_reverse('quest.views.view_question', args=(question.id, question.slug)))
        self.assertTrue(response)
        context = response.context[0]
        question = context.get('question')
        question_description = question.description
        for tag in settings.FILTER_HTML_TAGS.split(' '):
            self.assertFalse(tag in question_description)

class GiveAnswerTests(TestCase):
    fixtures = ['users.json', 'questions.json']

    def test_answer_page_fresh_access(self):
        question = Question.objects.latest()
        self.login_as(username='madhavbnk', password='nopassword')
        response = self.client.get(url_reverse('quest.views.view_give_answer', args=(question.id,)))
        self.assertRedirects(response,
                             expected_url=url_reverse('quest.views.view_question', args=(question.id, question.slug)),
                             status_code=302,
                             target_status_code=200)

    def test_answering_a_question(self):
        self.login_as(username='madhavbnk', password='nopassword')
        data = {'description':'My Answer goes like this'}
        question = Question.objects.latest()
        response = self.client.post(url_reverse('quest.views.view_give_answer', args=(question.id,)), data=data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'question.html')
        self.assertTemplateUsed(response, 'give_answer.html')
        context = response.context[0]
        self.assertTrue(context.has_key('question'))
        self.assertEquals(context.get('question').id, question.id)

    def test_answer_a_question_with_xss(self):
        self.login_as(username='madhavbnk', password='nopassword')
        data = {'description':'My Answer goes like this <script>alert("Hey");</script>'}
        question = Question.objects.latest()
        response = self.client.post(url_reverse('quest.views.view_give_answer', args=(question.id,)), data=data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        context = response.context[0]
        self.assertTrue(context.has_key('question'))
        question = context.get('question')
        answer = question.answers[0]
        self.assertNotEquals(answer.description, data['description'])
        self.assertFalse('script' in answer.description)

    def test_answering_a_question_with_blocked_tags(self):
        self.login_as(username='madhavbnk', password='nopassword')
        blocked_descriptions = ['I am giving a <marquee>fake</marquee> answer',
                                'This is also a fake <style>*{font-weight:120em;}</style>answer']
        question = Question.objects.latest()
        for description in blocked_descriptions:
            data = {'description':description}
            response = self.client.post(url_reverse('quest.views.view_give_answer', args=(question.id,)), data=data)
            self.assertTrue(response)
            self.assertEquals(response.status_code, 200)
            context = response.context[0]
            self.assertTrue(context.has_key('question'))
            question = context.get('question')
            answer = question.answers[0]
            self.assertNotEquals(answer.description, data['description'])
            for tag in settings.FILTER_HTML_TAGS.split(" "):
                self.assertFalse(tag in answer.description)