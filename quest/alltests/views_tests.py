from utils import TestCase
from django.core.urlresolvers import reverse as url_reverse
from quest.models import Question, Answer

class QuestionsPageTests(TestCase):
    def test_questions_page_fresh_access(self):
        #check anonymous, logged in
        raise NotImplementedError
    
    def test_each_question_page_fresh_access(self):
        raise NotImplementedError
    
    def test_invalid_url_to_question_page(self):
        raise NotImplementedError
    
class AskQuestionTests(TestCase):
    def test_ask_question_page_fresh_access(self):
        raise NotImplementedError
    
    def test_asking_a_question(self):
        #check anonymous, logged in
        raise NotImplementedError
    
    def test_asking_a_question_with_xss(self):
        raise NotImplementedError
    
    def test_asking_a_question_with_blocked_tags(self):
        raise NotImplementedError
    
    def test_close_answering_of_a_question(self):
        raise NotImplementedError
    
    def test_accept_an_answer_of_a_question(self):
        raise NotImplementedError
    
    def test_unaccepting_an_answer_of_a_question(self):
        raise NotImplementedError

class GiveAnswerTests(TestCase):
    fixtures = ['users.json', 'questions.json']
    
    def test_answer_page_fresh_access(self):
        raise NotImplementedError
    
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
        raise NotImplementedError
    
    def test_answering_a_question_with_blocked_tags(self):
        raise NotImplementedError