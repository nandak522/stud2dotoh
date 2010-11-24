from utils import TestCase
from django.core.urlresolvers import reverse as url_reverse
from quest.models import Question, Answer

class AskQuestionTests(TestCase):
    pass

class GiveAnswerTests(TestCase):
    fixtures = ['users.json', 'questions.json']
    
    def test_answering_question(self):
        self.login_as(username='madhavbnk', password='nopassword')
        data = {'description':'My Anwer goes like this'}
        question = Question.objects.latest()
        response = self.client.post(url_reverse('quest.views.view_give_answer', args=(question.id,)), data=data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'question.html')
        self.assertTemplateUsed(response, 'give_answer.html')
        context = response.context[0]
        self.assertTrue(context.has_key('question'))
        self.assertEquals(context.get('question').id, question.id)        